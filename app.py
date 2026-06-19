# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: The program starts the Flask application and
# displays the registration page


# Imports the Flask tools used to display pages and read forms
from flask import Flask, render_template, request

# Imports the registration validation function
from securepass.registration import validate_registration


# Creates the Flask application
app = Flask(__name__)

# Displays and processes the registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    # Creates an empty list to store registration messages
    messages = []

    # Creates empty values for the registration form
    username = ""
    email = ""

    # Checks if the registration form was submitted
    if request.method == "POST":

        # Gets the username entered in the form
        username = request.form.get("username", "")

        # Gets the email entered in the form
        email = request.form.get("email", "")

        # Gets the password entered in the form
        password = request.form.get("password", "")

        # Gets the confirmation password entered in the form
        confirm_password = request.form.get("confirm_password", "")

        # Calls the validation function and stores the result
        validation_result = validate_registration(
            username,
            email,
            password,
            confirm_password
        )

        # Stores the validation messages
        messages = validation_result["messages"]

        # Shows a temporary message when the information is valid
        if validation_result["is_valid"] == True:
            messages = [
                "Registration information is valid. "
                "The account has not been saved yet."
            ]

    # Displays the registration page with its current information
    return render_template(
        "register.html",
        messages=messages,
        username=username,
        email=email
    )


# Starts the Flask application when this file is run directly
if __name__ == "__main__":
    app.run()