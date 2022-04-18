from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fgn.db")


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
    """Index page to explain the webapp"""
    userinfo = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    user = userinfo[0]["username"].capitalize()
    return render_template("index.html", user=user)


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


@app.route("/games", methods=["GET", "POST"])
@login_required
def games():
    """Your games list"""
    if request.method == "POST":

        game = request.form.get("game")
        delete_game = request.form.get("delete_game")
        if not game:
            if delete_game:
                db.execute("DELETE FROM games WHERE game = ?", delete_game)
        else:
            db.execute("INSERT INTO games (id, game) VALUES(?, ?)", session["user_id"], game.capitalize())
        return redirect("/games")

    else:

        games = db.execute("SELECT * FROM games WHERE id = ?", session["user_id"])
        return render_template("games.html", games=games)


@app.route("/family", methods=["GET", "POST"])
@login_required
def family():
    """Your family members"""
    if request.method == "POST":

        name = request.form.get("name")
        delete_name = request.form.get("delete_name")
        if not name:
            if delete_name:
                db.execute("DELETE FROM family WHERE name = ?", delete_name)
        else:
            db.execute("INSERT INTO family (id, name) VALUES(?, ?)", session["user_id"], name.capitalize())
        return redirect("/family")

    else:

        family = db.execute("SELECT * FROM family WHERE id = ?", session["user_id"])

        return render_template("family.html", family=family)


@app.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboard():
    """Track the leaders"""
    if request.method == "POST":

        name = request.form.get("name")
        game = request.form.get("game")
        if not name or not game:
            return redirect("/leaderboard")
        else:
            db.execute("INSERT INTO leaderboard (id, game, winner) VALUES(?, ?, ?)", session["user_id"], game, name)
            return redirect("/leaderboard")

    else:
        family = db.execute("SELECT * FROM family WHERE id = ?", session["user_id"])
        games = db.execute("SELECT * FROM games WHERE id = ?", session["user_id"])
        leaders = db.execute("SELECT winner, COUNT(winner) FROM leaderboard WHERE id = ? GROUP BY winner ORDER BY COUNT(winner) DESC", session["user_id"])
        history = db.execute("SELECT winner, game, date FROM leaderboard WHERE id = ? ORDER BY date DESC", session["user_id"])
        return render_template("leaderboard.html", family=family, games=games, leaders=leaders, history=history)


@app.route("/spin", methods=["GET", "POST"])
@login_required
def spin():
    """The Wheel!"""
    options = db.execute("SELECT game FROM games WHERE id = ?", session["user_id"])
    options = [d['game'] for d in options]
    return render_template("spin.html", options=options)


##Generic app route
@app.route("/generic", methods=["GET", "POST"])
@login_required
def generic():
    """Comment here"""
    return apology("TODO")
