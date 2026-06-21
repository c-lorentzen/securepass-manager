# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_registration_route.py
# Program description: The program automatically tests Registration,
# duplicate checks, password hashing, and database storage


# Imports the operating system module to remove the test database
import os

# Imports the Flask application
from app import app

# Imports the Database functions used during testing
from securepass.database import initialize_database
from securepass.database import create_user
from securepass.database import get_user_by_login

# Imports the Security functions used during testing
from security_utils import hash_password
from security_utils import verify_password


# Stores the database used only for Registration route tests
TEST_DATABASE_PATH = "test_registration_routes.db"


# Removes the test database when it exists
def remove_test_database():

    # Checks if the test database exists
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)

    # Stores the possible SQLite journal file name
    journal_path = TEST_DATABASE_PATH + "-journal"

    # Checks if the journal file exists
    if os.path.exists(journal_path):
        os.remove(journal_path)


# Creates a fresh database before every test
def setup_function():

    # Removes information left by another test
    remove_test_database()

    # Uses testing mode
    app.config["TESTING"] = True

    # Uses the Registration test database
    app.config["DATABASE_PATH"] = TEST_DATABASE_PATH

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)


# Removes the database after every test
def teardown_function():

    # Restores the normal database path
    app.config["DATABASE_PATH"] = "securepass.db"

    # Removes the completed test database
    remove_test_database()


# Tests that the Registration page opens correctly
def test_registration_page_loads():

    # Creates a Flask test client
    test_client = app.test_client()

    # Opens the Registration page
    response = test_client.get("/register")

    # Checks that the page loaded
    assert response.status_code == 200

    # Checks that the page contains the main heading
    assert b"Create Account" in response.data


# Tests submitting the Registration form with empty fields
def test_registration_form_empty_fields():

    # Creates a Flask test client
    test_client = app.test_client()

    # Submits empty Registration information
    response = test_client.post(
        "/register",
        data={
            "username": "",
            "email": "",
            "password": "",
            "confirm_password": ""
        }
    )

    # Checks the required field messages
    assert b"Please enter a username." in response.data
    assert b"Please enter an email address." in response.data
    assert b"Please enter a password." in response.data
    assert b"Please confirm your password." in response.data


# Tests that valid Registration information creates a user
def test_registration_form_valid_information():

    # Creates a Flask test client
    test_client = app.test_client()

    # Stores the fictional password
    password = "Password123"

    # Submits valid Registration information
    response = test_client.post(
        "/register",
        data={
            "username": "studentUser",
            "email": "student@email.com",
            "password": password,
            "confirm_password": password
        },
        follow_redirects=True
    )

    # Checks that the user was redirected to Login
    assert response.status_code == 200

    # Checks that the successful Registration message was displayed
    assert b"Account created successfully. Please log in." in response.data

    # Gets the user from the test database
    user = get_user_by_login(
        "studentUser",
        TEST_DATABASE_PATH
    )

    # Checks that the user was stored
    assert user is not None

    # Checks that the original password was not stored
    assert user[3] != password

    # Checks that the stored password hash is valid
    assert verify_password(password, user[3]) == True


# Tests that a duplicate username is rejected
def test_duplicate_username_is_rejected():

    # Creates the first fictional user
    create_user(
        "existingUser",
        "first@email.com",
        hash_password("Password123"),
        TEST_DATABASE_PATH
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to register the same username
    response = test_client.post(
        "/register",
        data={
            "username": "existingUser",
            "email": "second@email.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
    )

    # Checks that the duplicate username message was displayed
    assert b"Username is already registered." in response.data


# Tests that a duplicate email is rejected
def test_duplicate_email_is_rejected():

    # Creates the first fictional user
    create_user(
        "firstUser",
        "existing@email.com",
        hash_password("Password123"),
        TEST_DATABASE_PATH
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to register the same email
    response = test_client.post(
        "/register",
        data={
            "username": "secondUser",
            "email": "existing@email.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
    )

    # Checks that the duplicate email message was displayed
    assert b"Email is already registered." in response.data