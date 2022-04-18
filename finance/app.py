import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT symbol, name, SUM(shares) FROM main WHERE id = ? GROUP BY symbol", session["user_id"])
    total = 0.00
    for row in rows:
        stockinfo = lookup(row["symbol"])
        total += float(row["SUM(shares)"] * stockinfo.get("price"))
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]
    return render_template("index.html", rows=rows, lookup=lookup, cash=cash, total=cash + total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        stockinfo = lookup(request.form.get("symbol"))
        if (stockinfo == None):
            return apology("not a valid stock", 400)
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("enter a valid number of shares", 400)

        if not isinstance(shares, int) or shares <= 0:
            return apology("enter a valid number of shares", 400)
        startcash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        startcash = startcash[0]["cash"]
        totalpurchase = shares * stockinfo.get('price')

        if (totalpurchase > startcash):
            return apology("you can't afford that", 400)

        db.execute("INSERT INTO main (id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], stockinfo.get('symbol'), stockinfo.get('name'), shares, stockinfo.get('price'))
        newcash = startcash - (stockinfo.get('price') * shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, dt FROM main WHERE id = ?", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """User Account Info"""
    if request.method == "POST":
        try:
            addfunds = int(request.form.get("addfunds"))
        except ValueError:
            return apology("enter a valid amount", 400)
        if not isinstance(addfunds, int) or addfunds <= 0:
            return apology("enter a valid amount", 400)
        startcash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        startcash = startcash[0]["cash"]
        newcash = startcash + addfunds
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, session["user_id"])
        return redirect("/")
    else:
        return render_template("account.html",)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stockinfo = lookup(request.form.get("symbol"))
        if (stockinfo != None):
            price = stockinfo.get('price')
            name = stockinfo.get('name')
            return render_template("quote.html", price=price, name=name)
        else:
            return apology("invalid ticker", 400)
    else:
        return render_template("quote.html", price=0, name="Look up a stock price!")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        elif (request.form.get("password")) != (request.form.get("confirmation")):
            return apology("password and confirmation must match", 400)

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username is unique, if so register user and login
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            return redirect("/")
        except ValueError:
            return apology("username already in use", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbols = db.execute("SELECT symbol FROM main GROUP BY symbol HAVING id = ?", session["user_id"])
    if request.method == "POST":

        stockinfo = lookup(request.form.get("symbol"))
        if (stockinfo == None):
            return apology("not a valid stock", 400)
        try:
            shares = -int(request.form.get("shares"))
        except ValueError:
            return apology("enter a valid number of shares", 400)

        currentsell = db.execute("SELECT SUM(shares) FROM main GROUP BY symbol HAVING id = ? AND symbol = ?",
                                 session["user_id"], stockinfo.get("symbol"))
        if currentsell[0]["SUM(shares)"] < -shares:
            return apology("you don't own that many shares", 400)

        startcash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        startcash = startcash[0]["cash"]

        db.execute("INSERT INTO main (id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], stockinfo.get('symbol'), stockinfo.get('name'), shares, stockinfo.get('price'))
        newcash = startcash - (stockinfo.get('price') * shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, session["user_id"])
        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)
