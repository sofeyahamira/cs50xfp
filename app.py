import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tracker.db")

# Custom filter
app.jinja_env.globals.update(str=str)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/landing")
        return f(*args, **kwargs)

    return decorated_function

# Routes
@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/")
@login_required
def index():
    # Get the usersname
    try:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    except IndexError:
        return redirect('/login')

    # Get variables
    balance = db.execute("SELECT balance FROM users WHERE id = ?", session["user_id"])[0]["balance"]
    logbook = db.execute("SELECT * FROM logbook WHERE user_id = ? ORDER BY log_time DESC", session["user_id"])

    return render_template("index.html", username=username, balance=balance, logbook=logbook)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", missing_username=True)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", missing_password=True)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("login.html", error_username=True)

        elif not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", error_password=True)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Get variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmation")

        # Ensure username not empty
        if (
            (len(username) == 0)
            or (len(username.strip()) == 0)
        ):
            return render_template("register.html", empty_username=True)

        # Ensure password not empty
        if (
            (len(password) == 0)
            or (len(password.strip()) == 0)
        ):
            return render_template("register.html", empty_password=True)

        # Ensure passwords match
        if password != confirmed_password:
            return render_template("register.html", unmatch_password=True)

        # Add user to database
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password),
            )

            # Redirect
            return redirect("/login")

        except ValueError:
            return render_template("register.html", used_username=True)
    else:
        return render_template("register.html")

@app.route("/settings")
@login_required
def settings():
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("settings.html", username=username)

@app.route("/log", methods=["GET", "POST"])
@login_required
def log():

    if request.method == "POST":

        # Define variables
        select_options = ['spent', 'recieved']
        transaction_type = request.form.get('transaction_type')
        notes = request.form.get('notes')
        amount = request.form.get('amount')
        user_balance = db.execute("SELECT balance FROM users WHERE id = ?", session["user_id"])[0]["balance"]

        # Ensure fields are not empty/invalid
        if not transaction_type:
            return render_template("log.html", empty_option=True)
        elif transaction_type not in select_options:
            return render_template("log.html", invalid_option=True)
        elif not notes:
            return render_template("log.html", missing_notes=True)
        elif not amount:
            return render_template("log.html", missing_amount=True)

        # Ensure amount is a number
        try:
            amount = int(amount)
        except ValueError:
            return render_template("log.html", invalid_amount=True)

        # Enusure amount is not too much
        if amount > user_balance and transaction_type == 'spent':
            return render_template("log.html", not_enough=True)
        elif amount > 1000000:
            return render_template("log.html", exceed_limit=True)

        # Update Logbook
        db.execute("INSERT INTO logbook (user_id, type, note, amount) VALUES (?, ?, ?, ?)",
                    session['user_id'], transaction_type, notes, amount)

        # Update users balance
        if transaction_type == 'spent':
            user_balance -= amount
            db.execute("UPDATE users SET balance = ? WHERE id = ?", user_balance, session["user_id"])
        else:
            user_balance += amount
            db.execute("UPDATE users SET balance = ? WHERE id = ?", user_balance, session["user_id"])

        return redirect("/")

    else:
        return render_template("log.html")

@app.route("/savings")
@login_required
def savings():
    # Get savings table
    try:
        savings_table = db.execute("SELECT * FROM savings WHERE user_id = ?", session["user_id"])[0]
    except IndexError:
        return redirect("savings_edit")

    # Return
    return render_template("savings.html", savings_table=savings_table)

@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to landing page
    return redirect("/landing")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        # Get all variables
        old_password = request.form.get("old_password")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmation")
        print(old_password, password, confirmed_password)

        # Find the user in the database
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )

        # Ensure password is correct
        print(rows)
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], old_password
        ):
            return render_template("change_password.html", wrong_password=True)

        # Ensure password not empty
        if (
            (len(password) == 0)
            or (len(password.strip()) == 0)
        ):
            return render_template("change_password.html", empty_password=True)

        # Ensure passwords match
        if password != confirmed_password:
            return render_template("change_password.html", unmatch_password=True)

        # Change password
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(password),
            session["user_id"],
        )

        # Redirect
        return redirect("/settings")

    else:
        return render_template("change_password.html")


@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("delete_account.html", missing_username=True)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("delete_account.html", missing_password=True)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )

        # Ensure username is correct
        if rows[0]["username"] != request.form.get("username"):
            return render_template("delete_account.html", error_username=True)

        # Ensure password is correct
        elif not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("delete_account.html", error_password=True)

        # Delete account from database
        db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
        db.execute("DELETE FROM savings WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM logbook WHERE user_id = ?", session["user_id"])

        # Redirect
        return redirect("/landing")
    else:
        return render_template("delete_account.html")

@app.route("/savings_edit", methods=["GET", "POST"])
@login_required
def savings_edit():
    if request.method == "POST":
        # Get variables
        amount = request.form.get('amount')
        saving_up_for = request.form.get('saving_up_for')
        required_savings = request.form.get('required_savings')
        user_balance = db.execute("SELECT balance FROM users WHERE id = ?", session["user_id"])[0]["balance"]

        # Ensurings fields not empty
        if not amount:
            amount = 0
        if not saving_up_for:
            saving_up_for = "Not saving up for anything"
        if not required_savings:
            required_savings = 0

        # Ensure amount is a number
        try:
            amount = int(amount)
        except ValueError:
            return render_template("savings_edit.html", invalid_amount=True)

        # Ensure required_savings is a number
        try:
            required_savings = int(required_savings)
        except ValueError:
            return render_template("savings_edit.html", invalid_req_amount=True)

        # Enusure amount is not too much
        if amount > user_balance:
            return render_template("savings_edit.html", not_enough=True)

        # Add data into database
        try:
            db.execute("""INSERT INTO savings (user_id, amount_in_savings, saving_up_for, required_savings)
                   VALUES (?, ?, ?, ?)""", session["user_id"], amount, saving_up_for, required_savings)
        except ValueError:
            db.execute("""UPDATE savings SET amount_in_savings = ?, saving_up_for = ?, required_savings = ?""",
                       amount, saving_up_for, required_savings)

        # Redirect
        return redirect("/savings")
    else:
        return render_template("savings_edit.html")
