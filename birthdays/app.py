import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")

        # Check if name already in database
        existing_names = db.execute('SELECT COUNT(*) FROM birthdays WHERE name=?', [name])

        if existing_names[0]["COUNT(*)"] == 0:
            db.execute(f'INSERT INTO birthdays (name,day,month) VALUES ("{name}",{day},{month});')
            return redirect("/")
        else:
            error = 'Name already in database'
            return render_template("error.html", name=name)


    else:

        # TODO: Display the entries in the database on index.html

        users = db.execute("SELECT * FROM birthdays ORDER BY name ;")

        return render_template("index.html", users=users)

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    db.execute(f'DELETE FROM birthdays WHERE name="{name}";')

    return redirect("/")

@app.route("/edit", methods=["POST"])
def edit():
    name = request.form.get("name")
    day = request.form.get("day")
    month = request.form.get("month")

    db.execute(f'UPDATE birthdays SET day={day},month={month} WHERE name="{name}";')

    return redirect("/")