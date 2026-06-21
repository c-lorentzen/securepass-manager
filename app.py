from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from securepass.authentication import AuthenticationService

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"   # Required for sessions

auth_service = AuthenticationService()


def is_user_logged_in():
    return "user_id" in session


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not is_user_logged_in():
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username_or_email = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # Check login using AuthenticationService (returns True/False)
    is_valid = auth_service.authenticate_user(username_or_email, password)

    if not is_valid:
        return render_template("login.html", error="Invalid username/email or password.")

    # TEMPORARY SESSION VALUES (until database integration)
    session["user_id"] = 1
    session["username"] = username_or_email

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    username = session.get("username")
    return f"""
    <h1>Welcome, {username}!</h1>
    <p>This is the dashboard.</p>
    <a href='{url_for("logout")}' style='
        display:inline-block;
        padding:8px 14px;
        background:#d9534f;
        color:white;
        text-decoration:none;
        border-radius:4px;
        font-weight:bold;
    '>Logout</a>
"""


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return "Registration page placeholder"


if __name__ == "__main__":
    app.run(debug=True)
