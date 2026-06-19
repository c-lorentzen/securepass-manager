# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Component: Registration


# Imports the regular expression module to check the email format
import re


# Validates the information entered in the registration form
def validate_registration(username, email, password, confirm_password):

    # Creates an empty list to store all the error messages
    error_messages = []

    # Checks if the username parameter is a string
    if type(username) != str:
        error_messages.append("Username must be text.")

    # Checks if the email parameter is a string
    if type(email) != str:
        error_messages.append("Email must be text.")

    # Checks if the password parameter is a string
    if type(password) != str:
        error_messages.append("Password must be text.")

    # Checks if the confirm password parameter is a string
    if type(confirm_password) != str:
        error_messages.append("Confirm password must be text.")

    # Returns the result early if any parameter has an invalid type
    if len(error_messages) > 0:

        # Stores False because the registration information is not valid
        is_valid = False

        # Creates a dictionary with the result and the error messages
        validation_result = {
            "is_valid": is_valid,
            "messages": error_messages
        }

        # Returns the dictionary before checking the rest of the information
        return validation_result

    # Removes extra spaces from the beginning and end of the username
    username = username.strip()

    # Removes extra spaces from the beginning and end of the email
    email = email.strip()

    # Checks if the username is empty
    if username == "":
        error_messages.append("Please enter a username.")

    # Checks if the email is empty
    if email == "":
        error_messages.append("Please enter an email address.")

    # Checks if the password is empty
    if password == "":
        error_messages.append("Please enter a password.")

    # Checks if the confirm password is empty
    if confirm_password == "":
        error_messages.append("Please confirm your password.")

    # Creates the pattern used to check the email format
    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    # Checks the email against the email pattern
    email_match = re.match(email_pattern, email)

    # Only checks the email format when the email is not empty
    if email != "":

        # Adds an error message when the email does not match the pattern
        if email_match is None:
            error_messages.append(
                "Please enter a valid email address."
            )

    # Only checks the password rules when the password is not empty
    if password != "":

        # Creates variables to store whether each password rule was found
        has_uppercase_letter = False
        has_lowercase_letter = False
        has_number = False

        # Checks every character in the password
        for character in password:

            # Checks if the current character is an uppercase letter
            if character.isupper():
                has_uppercase_letter = True

            # Checks if the current character is a lowercase letter
            if character.islower():
                has_lowercase_letter = True

            # Checks if the current character is a number
            if character.isdigit():
                has_number = True

        # Checks if the password has at least 8 characters
        if len(password) < 8:
            error_messages.append(
                "Password must be at least 8 characters long."
            )

        # Checks if the password has an uppercase letter
        if has_uppercase_letter == False:
            error_messages.append(
                "Password must contain at least one uppercase letter."
            )

        # Checks if the password has a lowercase letter
        if has_lowercase_letter == False:
            error_messages.append(
                "Password must contain at least one lowercase letter."
            )

        # Checks if the password has a number
        if has_number == False:
            error_messages.append(
                "Password must contain at least one number."
            )

    # Only compares the passwords when both fields are not empty
    if password != "" and confirm_password != "":

        # Checks if the password fields contain different values
        if password != confirm_password:
            error_messages.append("Passwords do not match.")

    # Stores True when the error messages list is empty
    is_valid = len(error_messages) == 0

    # Creates a dictionary with the final result and error messages
    validation_result = {
        "is_valid": is_valid,
        "messages": error_messages
    }

    # Returns the final validation result
    return validation_result