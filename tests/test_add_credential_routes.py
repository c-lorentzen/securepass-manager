# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_add_credential_routes.py
# Program description: The program automatically tests adding encrypted
# credentials through the SecurePass Manager application


# Imports the operating system module for test configuration
import os

# Imports Fernet to create a testing encryption key
from cryptography.fernet import Fernet

# Imports the Flask application
from app import app

# Imports the database functions used during testing
from securepass.database import initialize_database
from securepass.database import create_user
from securepass.database import get_user_by_login
from securepass.database import get_credentials_by_user

# Imports the security functions used during testing
from security_utils import hash_password
from security_utils import decrypt_password


# Stores the database used only during Add Credential testing
TEST_DATABASE_PATH = "test_add_credential.db"

# Creates one encryption key used by the automated tests
TEST_ENCRYPTION_KEY = Fernet.generate_key().decode()

# Stores the original environment encryption key
ORIGINAL_ENCRYPTION_KEY = os.environ.get("SECUREPASS_KEY")


# Removes the test database when it exists
def remove_test_database():

    # Checks if the test database exists
    if os.path.exists(TEST_DATABASE_PATH):

        # Removes the test database
        os.remove(TEST_DATABASE_PATH)

    # Stores the possible SQLite journal file name
    journal_path = TEST_DATABASE_PATH + "-journal"

    # Checks if the journal file exists
    if os.path.exists(journal_path):

        # Removes the journal file
        os.remove(journal_path)


# Creates a fresh database before every test
def setup_function():

    # Removes information left by another test
    remove_test_database()

    # Uses Flask testing mode
    app.config["TESTING"] = True

    # Uses the Add Credential test database
    app.config["DATABASE_PATH"] = TEST_DATABASE_PATH

    # Uses the fictional encryption key
    os.environ["SECUREPASS_KEY"] = TEST_ENCRYPTION_KEY

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)


# Removes testing information after every test
def teardown_function():

    # Restores the normal database path
    app.config["DATABASE_PATH"] = "securepass.db"

    # Restores the original encryption key
    if ORIGINAL_ENCRYPTION_KEY is None:
        os.environ.pop("SECUREPASS_KEY", None)
    else:
        os.environ["SECUREPASS_KEY"] = ORIGINAL_ENCRYPTION_KEY

    # Removes the completed test database
    remove_test_database()


# Creates two fictional users and returns their IDs
def create_test_users():

    # Creates the first fictional user
    create_user(
        "firstUser",
        "first@email.com",
        hash_password("Password123"),
        TEST_DATABASE_PATH
    )

    # Creates the second fictional user
    create_user(
        "secondUser",
        "second@email.com",
        hash_password("Password456"),
        TEST_DATABASE_PATH
    )

    # Gets the first user
    first_user = get_user_by_login(
        "firstUser",
        TEST_DATABASE_PATH
    )

    # Gets the second user
    second_user = get_user_by_login(
        "secondUser",
        TEST_DATABASE_PATH
    )

    # Returns both user IDs
    return first_user[0], second_user[0]


# Stores a fictional user inside the Flask session
def log_in_test_user(test_client, user_id, username):

    # Opens the Flask testing session
    with test_client.session_transaction() as test_session:

        # Stores the fictional user ID
        test_session["user_id"] = user_id

        # Stores the fictional username
        test_session["username"] = username


# Tests that a logged-out user cannot open Add Credential
def test_add_credential_requires_login():

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open Add Credential
    response = test_client.get("/credentials/add")

    # Checks that the user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that a logged-in user can open Add Credential
def test_add_credential_page_loads():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Opens Add Credential
    response = test_client.get("/credentials/add")

    # Checks that the page loaded
    assert response.status_code == 200

    # Checks that the heading is displayed
    assert b"Add Credential" in response.data

    # Checks that the form button is displayed
    assert b"Save Credential" in response.data


# Tests validation of the required fields
def test_add_credential_required_fields():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Submits empty credential information
    response = test_client.post(
        "/credentials/add",
        data={
            "website": "",
            "website_url": "",
            "login_username": "",
            "saved_password": "",
            "notes": ""
        }
    )

    # Checks the required website message
    assert b"Please enter the website or account name." in response.data

    # Checks the required username message
    assert b"Please enter the account username or email." in response.data

    # Checks the required password message
    assert b"Please enter the password you want to save." in response.data


# Tests that a credential is stored using encryption
def test_add_credential_stores_encrypted_password():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Stores the fictional password
    saved_password = "SavedPassword123"

    # Submits valid credential information
    response = test_client.post(
        "/credentials/add",
        data={
            "website": "Student Portal",
            "website_url": "https://student.example.com",
            "login_username": "studentUser",
            "saved_password": saved_password,
            "notes": "School account"
        }
    )

    # Checks that the user was redirected to the Dashboard
    assert response.status_code == 302
    assert "/dashboard" in response.location

    # Gets the first user's credentials
    credentials = get_credentials_by_user(
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that one credential was created
    assert len(credentials) == 1

    # Stores the created credential
    credential = credentials[0]

    # Checks the saved website
    assert credential["website"] == "Student Portal"

    # Checks the saved username
    assert credential["username"] == "studentUser"

    # Checks that the original password was not stored
    assert credential["encrypted_password"] != saved_password

    # Checks that the encrypted password can be decrypted correctly
    assert decrypt_password(
        credential["encrypted_password"]
    ) == saved_password


# Tests that the credential belongs only to the current user
def test_add_credential_uses_current_user_id():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Creates a credential
    test_client.post(
        "/credentials/add",
        data={
            "website": "Private Account",
            "website_url": "https://private.example.com",
            "login_username": "privateUser",
            "saved_password": "PrivatePassword123",
            "notes": "Private information"
        }
    )

    # Gets the first user's credentials
    first_user_credentials = get_credentials_by_user(
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Gets the second user's credentials
    second_user_credentials = get_credentials_by_user(
        second_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the credential belongs to the first user
    assert len(first_user_credentials) == 1

    # Checks that the second user received no credential
    assert second_user_credentials == []


# Tests that the new credential appears on the Dashboard
def test_added_credential_appears_on_dashboard():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Creates a new credential
    response = test_client.post(
        "/credentials/add",
        data={
            "website": "Email Account",
            "website_url": "https://mail.example.com",
            "login_username": "emailUser",
            "saved_password": "EmailPassword123",
            "notes": "Personal email"
        },
        follow_redirects=True
    )

    # Checks that the Dashboard loaded
    assert response.status_code == 200

    # Checks that the website is displayed
    assert b"Email Account" in response.data

    # Checks that the username is displayed
    assert b"emailUser" in response.data

    # Checks that the original password is not displayed
    assert b"EmailPassword123" not in response.data

    # Checks that the password is masked
    assert b"**********" in response.data