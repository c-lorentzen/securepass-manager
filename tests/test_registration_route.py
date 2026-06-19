# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/19/2026
# Program title: test_registration_route.py
# Program description: The program automatically tests the
# Flask registration page and form


# Imports the Flask application that will be tested
from app import app


# Tests that the registration page opens correctly
def test_registration_page_loads():

    # Creates a test client for the Flask application
    test_client = app.test_client()

    # Sends a GET request to the registration page
    response = test_client.get("/register")

    # Stores the expected status code
    expected_status_code = 200

    # Checks that the page loaded successfully
    assert response.status_code == expected_status_code

    # Checks that the registration page contains the main heading
    assert b"Create Account" in response.data


# Tests submitting the registration form with empty fields
def test_registration_form_empty_fields():

    # Creates a test client for the Flask application
    test_client = app.test_client()

    # Creates the empty registration form information
    form_data = {
        "username": "",
        "email": "",
        "password": "",
        "confirm_password": ""
    }

    # Sends the empty information to the registration route
    response = test_client.post(
        "/register",
        data=form_data
    )

    # Stores the expected status code
    expected_status_code = 200

    # Checks that the page loaded successfully
    assert response.status_code == expected_status_code

    # Checks that the username error message was displayed
    assert b"Please enter a username." in response.data

    # Checks that the email error message was displayed
    assert b"Please enter an email address." in response.data

    # Checks that the password error message was displayed
    assert b"Please enter a password." in response.data

    # Checks that the confirmation error message was displayed
    assert b"Please confirm your password." in response.data


# Tests submitting valid registration information
def test_registration_form_valid_information():

    # Creates a test client for the Flask application
    test_client = app.test_client()

    # Creates valid registration form information
    form_data = {
        "username": "studentUser",
        "email": "student@email.com",
        "password": "Password123",
        "confirm_password": "Password123"
    }

    # Sends the valid information to the registration route
    response = test_client.post(
        "/register",
        data=form_data
    )

    # Stores the expected status code
    expected_status_code = 200

    # Checks that the page loaded successfully
    assert response.status_code == expected_status_code

    # Checks that the temporary valid registration message was displayed
    assert (
        b"Registration information is valid. "
        b"The account has not been saved yet."
        in response.data
    )