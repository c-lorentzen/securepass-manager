# Authors: Cristhian Lorentzen and Dylan Bloom
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: The program displays the Registration and Login
# pages and manages the authenticated user session


# Imports the operating system module to read configuration values
import os

# Imports the Flask tools used to display pages, read forms, and manage sessions
from flask import Flask, render_template, request, redirect, url_for, session

# Imports wraps so the protected route keeps its original name
from functools import wraps

# Imports the Registration validation function
from securepass.registration import validate_registration

# Imports the Authentication service
from securepass.authentication import AuthenticationService

# Imports the user database functions
from securepass.database import initialize_database
from securepass.database import username_exists
from securepass.database import email_exists
from securepass.database import create_user
from securepass.database import get_user_by_login

# Imports the password hashing function
from security_utils import hash_password


# Creates the Flask application
app = Flask(__name__)

# Reads the Flask secret key from an environment variable
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "development-secret-key"
)

# Stores the path used for the SQLite database
app.config["DATABASE_PATH"] = os.environ.get(
    "SECUREPASS_DATABASE_PATH",
    "securepass.db"
)

# Creates the database tables when they do not already exist
initialize_database(app.config["DATABASE_PATH"])


# Checks if a user ID is stored in the session
def is_user_logged_in():

    # Returns True if the user is logged in
    return "user_id" in session


# Protects pages that require a logged-in user
def login_required(view_function):

    # Keeps the original route function information
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        # Redirects the user if no user ID is in the session
        if is_user_logged_in() == False:
            return redirect(url_for("login"))

        # Displays the protected page
        return view_function(*args, **kwargs)

    # Returns the protected route function
    return wrapped_view


# Redirects the starting page to Login
@app.route("/")
def home():

    # Sends the user to the Login page
    return redirect(url_for("login"))


# Displays and processes the Registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    # Creates an empty list to store Registration messages
    messages = []

    # Creates empty values for the Registration form
    username = ""
    email = ""

    # Checks if the Registration form was submitted
    if request.method == "POST":

        # Gets and cleans the username entered in the form
        username = request.form.get("username", "").strip()

        # Gets and cleans the email entered in the form
        email = request.form.get("email", "").strip()

        # Gets the password entered in the form
        password = request.form.get("password", "")

        # Gets the confirmation password entered in the form
        confirm_password = request.form.get("confirm_password", "")

        # Stores the current database path
        database_path = app.config["DATABASE_PATH"]

        # Checks if the username already exists
        username_already_exists = False

        if username != "":
            username_already_exists = username_exists(
                username,
                database_path
            )

        # Checks if the email already exists
        email_already_exists = False

        if email != "":
            email_already_exists = email_exists(
                email,
                database_path
            )

        # Calls the validation function and stores the result
        validation_result = validate_registration(
            username,
            email,
            password,
            confirm_password,
            username_already_exists,
            email_already_exists
        )

        # Stores the validation messages
        messages = validation_result["messages"]

        # Continues when the Registration information is valid
        if validation_result["is_valid"] == True:

            # Creates a protected hash of the account password
            password_hash = hash_password(password)

            # Stores the new user in the database
            user_created = create_user(
                username,
                email,
                password_hash,
                database_path
            )

            # Sends the new user to Login when the account was created
            if user_created == True:
                return redirect(
                    url_for(
                        "login",
                        registered="true"
                    )
                )

            # Shows a safe message if the user could not be saved
            messages = [
                "The account could not be created. "
                "Please try again."
            ]

    # Displays the Registration page with its current information
    return render_template(
        "register.html",
        messages=messages,
        username=username,
        email=email
    )


# Displays and processes the Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Stores an empty success message
    success_message = ""

    # Checks if the user was redirected after Registration
    if request.args.get("registered") == "true":
        success_message = "Account created successfully. Please log in."

    # Displays the Login page before the form is submitted
    if request.method == "GET":
        return render_template(
            "login.html",
            success_message=success_message
        )

    # Gets the username or email entered in the form
    username_or_email = request.form.get("username", "").strip()

    # Gets the password entered in the form
    password = request.form.get("password", "")

    # Creates the Authentication service using the current database
    auth_service = AuthenticationService(
        app.config["DATABASE_PATH"]
    )

    # Checks the Login information
    is_valid = auth_service.authenticate_user(
        username_or_email,
        password
    )

    # Displays a safe message when the Login information is invalid
    if is_valid == False:
        return render_template(
            "login.html",
            error="Invalid username/email or password."
        )

    # Stores temporary user information in the session
    session["user_id"] = 1
    session["username"] = username_or_email

    # Sends the logged-in user to the Dashboard
    return redirect(url_for("dashboard"))


# Displays a temporary protected Dashboard
@app.route("/dashboard")
@login_required
def dashboard():

    # Gets the username stored in the session
    username = session.get("username", "")

    # Displays the temporary Dashboard
    return (
        "<h1>Welcome, " + username + "!</h1>"
        "<p>This is the dashboard.</p>"
        "<a href='/logout'>Logout</a>"
    )


# Logs the user out
@app.route("/logout")
def logout():

    # Removes all information from the session
    session.clear()

    # Sends the user back to the Login page
    return redirect(url_for("login"))


# Starts the Flask application when this file is run directly
if __name__ == "__main__":
    app.run()