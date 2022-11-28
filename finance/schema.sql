CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username_id INTEGER NOT NULL,
    type TEXT CHECK(
        type = "buy"
        or type = "sell"
    ),
    symbol TEXT NOT NULL,
    quantity NUMERIC NOT NULL,
    price REAL NOT NULL,
    date TEXT NOT NULL UNIQUE,
    FOREIGN KEY (username_id) REFERENCES users(id)
);
CREATE TABLE portfolios (
    username_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    quantity NUMERIC NOT NULL,
    FOREIGN KEY (username_id) REFERENCES users(id)
    UNIQUE(username_id, symbol)
);