import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import re

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        action = request.form.get("action")

        # print(f"Got request to {action} {symbol}")
        if action == "buy":
            return render_template("buy.html", stock=symbol)

        elif action == "sell":
            stocks = db.execute("SELECT symbol FROM portfolios WHERE username_id=? ORDER BY symbol", session["user_id"])
            if stocks:
                return render_template("sell.html", stocks=stocks, symbol=symbol)
            else:
                flash("You don't own any shares to sell")
                return redirect("/")
        else:
            return apology("Invalid symbol", 400)

    # Else it's a GET
    else:
        rows = db.execute("SELECT * from portfolios WHERE username_id=? ORDER BY symbol", session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        networth = cash
        for row in rows:
            row["price"] = lookup(row["symbol"])["price"]
            row["total"] = row["price"] * row["quantity"]
            networth += row["total"]

        return render_template("index.html", stocks=rows, cash=cash, networth=networth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("symbol must be provided", 400)

        try:
            shares = int(request.form.get("shares"))

        except:
            return apology("invald share value", 400)

        if shares < 1:
            return apology("minimum share value is 1", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        # At this point we have the correct symbol, price and share amount, so lets check balance
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

        cost = shares * quote["price"]

        if cash[0]["cash"] < cost:
            return apology("sorry, you don't have enough cash", 400)
        else:
            # All good, update orders
            db.execute("INSERT INTO orders (username_id, type, symbol, quantity, price, date) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                       session["user_id"], "buy", quote["symbol"], shares, quote["price"])

            # Update cash balance
            db.execute("UPDATE users SET cash=cash-? WHERE id=?", cost, session["user_id"])

            # Update porfolio
            stock_qty = db.execute("SELECT quantity FROM portfolios WHERE username_id=? and symbol=?", session["user_id"], symbol)

            if stock_qty:
                db.execute("UPDATE portfolios SET quantity=quantity+? WHERE username_id=? and symbol=?",
                           shares, session["user_id"], symbol)
            else:
                db.execute("INSERT INTO portfolios (username_id, symbol, quantity) VALUES (?, ?, ?)",
                           session["user_id"], symbol, shares)

        flash(f'Successfully bought {shares} {quote["symbol"]} shares at {usd(quote["price"])}', 200)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    orders = db.execute("SELECT * FROM orders WHERE username_id=? ORDER BY date", session["user_id"])

    return render_template("history.html", orders=orders)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/"), flash(f"Welcome back {rows[0]['username']} !", 200)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        quote = lookup(request.form.get("symbol").upper())

        # TODO : Implement multiple symbol quoting
        # If symbol is somehow invalid
        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted and matches
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password and confirmation", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)

        if not password_req(request.form.get("password")):
            return apology("password doesn't fill requirements", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) > 0:
            return apology("username already registered", 400)

        # Since password and username are good, we can insert it to the table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/"), flash(f"Welcome {request.form.get('username')}, you're now registered !", 200)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("symbol must be provided", 400)

        try:
            shares = int(request.form.get("shares"))

        except:
            return apology("invald share value", 400)

        if shares < 1:
            return apology("minimum share value is 1", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        # At this point we have the correct symbol, and share amount, so lets check if the user has enough to sell

        portfolio = db.execute("SELECT quantity FROM portfolios WHERE username_id=? and symbol=?",
                               session["user_id"], quote["symbol"])

        # If shares were found
        if portfolio:
            # If user has enough shares and can sell
            if portfolio[0]["quantity"] - shares >= 0:

                # All good, update orders
                db.execute("INSERT INTO orders (username_id, type, symbol, quantity, price, date) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                           session["user_id"], "sell", quote["symbol"], shares, quote["price"])

                # Update cash balance
                db.execute("UPDATE users SET cash=cash+? WHERE id=?", shares * quote["price"], session["user_id"])

                if portfolio[0]["quantity"] - shares == 0:
                    # If user is selling all shares, delete row from portfolio
                    db.execute("DELETE FROM portfolios WHERE username_id=? and symbol=?", session["user_id"], quote["symbol"])
                else:
                    # Otherwise update portfolio
                    db.execute("UPDATE portfolios SET quantity=quantity-? WHERE username_id=? and symbol=?",
                               shares, session["user_id"], quote["symbol"])

                flash(f'Successfully sold {shares} {quote["symbol"]} shares at {usd(quote["price"])}', 200)
                return redirect("/")

        # Not enough shares
        return apology("you don't have shares to sell")

    else:
        stocks = db.execute("SELECT symbol FROM portfolios WHERE username_id=? ORDER BY symbol", session["user_id"])
        if stocks:
            return render_template("sell.html", stocks=stocks)
        else:
            flash("You don't own any shares to sell")
            return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password"""

    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # Ensure password was submitted and matches database
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("current password is wrong", 400)

        # Ensure password was submitted and matches
        if not request.form.get("new_password") or not request.form.get("confirmation"):
            return apology("must provide password and confirmation", 400)

        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("new password and confirmation must match", 400)

        if not password_req(request.form.get("password")):
            return apology("password doesn't fill requirements", 400)

        # Update database for username password
        db.execute("UPDATE users SET hash=? WHERE id = ?",
                   generate_password_hash(request.form.get("new_password")), session["user_id"])

        flash("Password successfully changed")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Change user password"""

    if request.method == "POST":

        # Ensure cash amount was submitted correctly
        if not request.form.get("cash"):
            return apology("must fill amount of cash to be added", 400)

        try:
            cash = float(request.form.get("cash"))
        except:
            return apology("invalid cash amount", 400)

        if cash <= 0:
            return apology("invalid cash amount", 400)

        else:
            # Update database for username password
            db.execute("UPDATE users SET cash=cash+? WHERE id = ?", cash, session["user_id"])

            flash(f"You've successfully added {usd(cash)} .")
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get username cash
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        balance = balance[0]["cash"]
        return render_template("add_cash.html", balance=balance)


def password_req(psw):
    """Check if password fills requirements of at least :"""
    """8 characters, 1 digit, 1 symbol, 1 uppercase letter, 1 lowercase letter"""

    if re.fullmatch(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', psw):
        return True

    return False