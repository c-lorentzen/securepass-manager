# Authors: Elissa Schlosser and Cristhian Lorentzen
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_dashboard_routes.py
# Program description: The program automatically tests the Dashboard,
# credential search, authorized viewing, and user ownership protection


# Imports the operating system module for the test configuration
import os

# Imports Fernet to create a fictional testing key
from cryptography.fernet import Fernet

# Imports the Flask application
from app import app

# Imports the database functions used during testing
from securepass.database import initialize_database
from securepass.database import create_user
from securepass.database import get_user_by_login
from securepass.database import create_credential

# Imports the security functions used during testing
from security_utils import hash_password
from security_utils import encrypt_password


# Stores the database used only during Dashboard testing
TEST_DATABASE_PATH = "test_dashboard.db"

# Creates one encryption key used by the automated tests
TEST_ENCRYPTION_KEY = Fernet.generate_key().decode()

# Stores the original environment key
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

    # Uses the Dashboard test database
    app.config["DATABASE_PATH"] = TEST_DATABASE_PATH

    # Uses the fictional encryption key
    os.environ["SECUREPASS_KEY"] = TEST_ENCRYPTION_KEY

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)


# Removes the testing information after every test
def teardown_function():

    # Restores the normal database path
    app.config["DATABASE_PATH"] = "securepass.db"

    # Restores the original environment key
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


# Stores a logged-in user inside the Flask session
def log_in_test_user(test_client, user_id, username):

    # Opens the Flask testing session
    with test_client.session_transaction() as test_session:

        # Stores the fictional user ID
        test_session["user_id"] = user_id

        # Stores the fictional username
        test_session["username"] = username


# Creates a fictional encrypted credential
def create_test_credential(
    user_id,
    website,
    login_username,
    saved_password
):

    # Encrypts the fictional saved password
    encrypted_password = encrypt_password(saved_password)

    # Stores and returns the fictional credential
    return create_credential(
        user_id,
        website,
        "https://" + website.lower().replace(" ", "") + ".example.com",
        login_username,
        encrypted_password,
        "Fictional credential used during testing",
        TEST_DATABASE_PATH
    )


# Tests that a logged-out user cannot open the Dashboard
def test_dashboard_requires_login():

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open the Dashboard
    response = test_client.get("/dashboard")

    # Checks that the user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that the Dashboard displays only the current user's credentials
def test_dashboard_displays_only_current_user_credentials():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    create_test_credential(
        first_user_id,
        "Student Portal",
        "firstStudent",
        "FirstSavedPassword123"
    )

    # Creates a credential owned by the second user
    create_test_credential(
        second_user_id,
        "Private Bank",
        "secondBankUser",
        "SecondSavedPassword456"
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Opens the Dashboard
    response = test_client.get("/dashboard")

    # Checks that the Dashboard loaded
    assert response.status_code == 200

    # Checks that the first user's credential is displayed
    assert b"Student Portal" in response.data

    # Checks that the second user's credential is not displayed
    assert b"Private Bank" not in response.data

    # Checks that the saved password is masked on the Dashboard
    assert b"FirstSavedPassword123" not in response.data
    assert b"**********" in response.data


# Tests that Search returns only the current user's matching credential
def test_search_returns_only_current_user_results():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a matching credential for the first user
    create_test_credential(
        first_user_id,
        "School Email",
        "firstSchoolUser",
        "SchoolPassword123"
    )

    # Creates another credential for the first user
    create_test_credential(
        first_user_id,
        "Work Portal",
        "firstWorkUser",
        "WorkPassword123"
    )

    # Creates a matching credential for the second user
    create_test_credential(
        second_user_id,
        "School Administration",
        "secondSchoolUser",
        "OtherSchoolPassword"
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Searches for School
    response = test_client.get(
        "/search?query=School"
    )

    # Checks that the Search page loaded
    assert response.status_code == 200

    # Checks that the first user's matching credential is displayed
    assert b"School Email" in response.data

    # Checks that the nonmatching credential is not displayed
    assert b"Work Portal" not in response.data

    # Checks that the second user's credential is not displayed
    assert b"School Administration" not in response.data


# Tests the message displayed when Search finds no credential
def test_search_displays_no_results_message():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates one fictional credential
    create_test_credential(
        first_user_id,
        "Email Account",
        "emailUser",
        "EmailPassword123"
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Searches for information that does not exist
    response = test_client.get(
        "/search?query=UnknownCredential"
    )

    # Checks that the no-results message is displayed
    assert b"No matching credentials were found." in response.data


# Tests that the owner can view and decrypt a credential
def test_owner_can_view_decrypted_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(
        first_user_id,
        "Streaming Account",
        "streamUser",
        "StreamingPassword123"
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Opens the credential details page
    response = test_client.get(
        "/credentials/" + str(entry_id)
    )

    # Checks that the page loaded
    assert response.status_code == 200

    # Checks that the credential information is displayed
    assert b"Streaming Account" in response.data
    assert b"streamUser" in response.data

    # Checks that the password was correctly decrypted
    assert b"StreamingPassword123" in response.data


# Tests that another user cannot view the credential
def test_other_user_cannot_view_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the second user
    entry_id = create_test_credential(
        second_user_id,
        "Second User Account",
        "privateSecondUser",
        "PrivatePassword456"
    )

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Tries to open the second user's credential
    response = test_client.get(
        "/credentials/" + str(entry_id),
        follow_redirects=True
    )

    # Checks that the user returned to the Dashboard
    assert response.status_code == 200
    assert b"SecurePass Dashboard" in response.data

    # Checks that the other user's information was not exposed
    assert b"Second User Account" not in response.data
    assert b"privateSecondUser" not in response.data
    assert b"PrivatePassword456" not in response.data