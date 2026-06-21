# Author: Dylan Bloom
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_authentication_routes.py
# Program description: The program automatically tests Login,
# protected pages, sessions, and Logout


# Imports the operating system module to remove the test database
import os

# Imports the Flask application
from app import app

# Imports the database functions used during testing
from securepass.database import initialize_database
from securepass.database import create_user

# Imports the password hashing function
from security_utils import hash_password


# Stores the database used only for route tests
TEST_DATABASE_PATH = "test_authentication_routes.db"


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

    # Uses the route test database
    app.config["DATABASE_PATH"] = TEST_DATABASE_PATH

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)


# Removes the database after every test
def teardown_function():

    # Restores the normal database path
    app.config["DATABASE_PATH"] = "securepass.db"

    # Removes the completed test database
    remove_test_database()


# Creates the fictional user used by a route test
def create_test_user():

    # Creates a protected hash
    password_hash = hash_password("Password123")

    # Stores the fictional user
    create_user(
        "testUser",
        "test@email.com",
        password_hash,
        TEST_DATABASE_PATH
    )


# Tests that the Login page opens correctly
def test_login_page_loads_correctly():

    # Creates a Flask test client
    test_client = app.test_client()

    # Opens the Login page
    response = test_client.get("/login")

    # Checks that the page loaded
    assert response.status_code == 200

    # Checks that the Login heading is displayed
    assert b"Login" in response.data


# Tests that successful Login creates a real session
def test_session_created_after_successful_login():

    # Creates the fictional database user
    create_test_user()

    # Creates a Flask test client
    test_client = app.test_client()

    # Submits valid Login information
    response = test_client.post(
        "/login",
        data={
            "username": "testUser",
            "password": "Password123"
        }
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Opens the Flask session
    with test_client.session_transaction() as test_session:

        # Checks that the real database user ID was stored
        assert test_session["user_id"] == 1

        # Checks that the registered username was stored
        assert test_session["username"] == "testUser"

        # Checks that the password was not stored
        assert "password" not in test_session


# Tests that an unauthenticated user is blocked
def test_unauthenticated_user_blocked_from_protected_page():

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open the protected Dashboard
    response = test_client.get(
        "/dashboard",
        follow_redirects=True
    )

    # Checks that the user was redirected to Login
    assert b"Login" in response.data


# Tests that an authenticated user can open the protected Dashboard
def test_authenticated_user_can_access_protected_page():

    # Creates the fictional database user
    create_test_user()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in using valid information
    test_client.post(
        "/login",
        data={
            "username": "testUser",
            "password": "Password123"
        }
    )

    # Opens the protected Dashboard
    response = test_client.get("/dashboard")

    # Checks that the Dashboard loaded
    assert response.status_code == 200

    # Checks that the welcome message is displayed
    assert b"Welcome" in response.data

    # Checks that the registered username is displayed
    assert b"testUser" in response.data


# Tests that invalid Login information displays a safe message
def test_invalid_login_displays_safe_message():

    # Creates the fictional database user
    create_test_user()

    # Creates a Flask test client
    test_client = app.test_client()

    # Submits an incorrect password
    response = test_client.post(
        "/login",
        data={
            "username": "testUser",
            "password": "WrongPassword123"
        }
    )

    # Checks that the safe error message was displayed
    assert b"Invalid username/email or password." in response.data


# Tests that Logout removes the user session
def test_logout_removes_user_session():

    # Creates the fictional database user
    create_test_user()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in using valid information
    test_client.post(
        "/login",
        data={
            "username": "testUser",
            "password": "Password123"
        }
    )

    # Logs the user out
    test_client.get("/logout")

    # Opens the Flask session
    with test_client.session_transaction() as test_session:

        # Checks that the user ID was removed
        assert "user_id" not in test_session

        # Checks that the username was removed
        assert "username" not in test_session

    # Tries to open the Dashboard after Logout
    response = test_client.get(
        "/dashboard",
        follow_redirects=True
    )

    # Checks that the user returned to Login
    assert b"Login" in response.data