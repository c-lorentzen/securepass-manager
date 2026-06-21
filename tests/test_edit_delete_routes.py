# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_edit_delete_routes.py
# Program description: The program automatically tests editing and
# deleting credentials through SecurePass Manager


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
from securepass.database import create_credential
from securepass.database import get_credential_by_id

# Imports the security functions used during testing
from security_utils import hash_password
from security_utils import encrypt_password
from security_utils import decrypt_password


# Stores the database used only during Edit and Delete testing
TEST_DATABASE_PATH = "test_edit_delete.db"

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

    # Uses the Edit and Delete test database
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

    # Gets the first fictional user
    first_user = get_user_by_login(
        "firstUser",
        TEST_DATABASE_PATH
    )

    # Gets the second fictional user
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


# Creates an encrypted credential and returns its ID
def create_test_credential(user_id):

    # Encrypts the original fictional password
    encrypted_password = encrypt_password(
        "OriginalPassword123"
    )

    # Creates and returns the credential ID
    return create_credential(
        user_id,
        "Original Website",
        "https://original.example.com",
        "originalUser",
        encrypted_password,
        "Original notes",
        TEST_DATABASE_PATH
    )


# Tests that a logged-out user cannot open Edit Credential
def test_edit_credential_requires_login():

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open Edit Credential
    response = test_client.get("/credentials/1/edit")

    # Checks that the user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that the credential owner can open the Edit page
def test_owner_can_open_edit_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Opens the Edit Credential page
    response = test_client.get(
        "/credentials/" + str(entry_id) + "/edit"
    )

    # Checks that the page loaded
    assert response.status_code == 200

    # Checks that the heading is displayed
    assert b"Edit Credential" in response.data

    # Checks that the current website is displayed
    assert b"Original Website" in response.data

    # Checks that the current username is displayed
    assert b"originalUser" in response.data


# Tests that an empty password field keeps the current password
def test_edit_keeps_existing_password_when_field_is_empty():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Gets the original credential
    original_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Stores the original encrypted password
    original_encrypted_password = original_credential[
        "encrypted_password"
    ]

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Updates the credential without entering a new password
    response = test_client.post(
        "/credentials/" + str(entry_id) + "/edit",
        data={
            "website": "Updated Website",
            "website_url": "https://updated.example.com",
            "login_username": "updatedUser",
            "saved_password": "",
            "notes": "Updated notes"
        }
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Gets the updated credential
    updated_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the website was updated
    assert updated_credential["website"] == "Updated Website"

    # Checks that the username was updated
    assert updated_credential["username"] == "updatedUser"

    # Checks that the encrypted password was not changed
    assert (
        updated_credential["encrypted_password"]
        == original_encrypted_password
    )

    # Checks that the original password still decrypts correctly
    assert decrypt_password(
        updated_credential["encrypted_password"]
    ) == "OriginalPassword123"


# Tests that a replacement password is encrypted
def test_edit_encrypts_replacement_password():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Stores the new fictional password
    new_password = "ReplacementPassword456"

    # Updates the credential using a new password
    response = test_client.post(
        "/credentials/" + str(entry_id) + "/edit",
        data={
            "website": "Original Website",
            "website_url": "https://original.example.com",
            "login_username": "originalUser",
            "saved_password": new_password,
            "notes": "Original notes"
        }
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Gets the updated credential
    updated_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the original text was not stored
    assert (
        updated_credential["encrypted_password"]
        != new_password
    )

    # Checks that the replacement password decrypts correctly
    assert decrypt_password(
        updated_credential["encrypted_password"]
    ) == new_password


# Tests that Delete Credential does not accept GET
def test_delete_credential_requires_post():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Tries to delete using GET
    response = test_client.get(
        "/credentials/" + str(entry_id) + "/delete"
    )

    # Checks that GET is not allowed
    assert response.status_code == 405

    # Checks that the credential still exists
    credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that GET did not delete the credential
    assert credential is not None


# Tests that the owner can delete a credential
def test_owner_can_delete_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the first user
    log_in_test_user(
        test_client,
        first_user_id,
        "firstUser"
    )

    # Deletes the credential using POST
    response = test_client.post(
        "/credentials/" + str(entry_id) + "/delete"
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to the Dashboard
    assert "/dashboard" in response.location

    # Tries to retrieve the deleted credential
    deleted_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the credential was deleted
    assert deleted_credential is None


# Tests that another user cannot edit the credential
def test_other_user_cannot_edit_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the second user
    log_in_test_user(
        test_client,
        second_user_id,
        "secondUser"
    )

    # Tries to edit the first user's credential
    response = test_client.post(
        "/credentials/" + str(entry_id) + "/edit",
        data={
            "website": "Unauthorized Website",
            "website_url": "https://unauthorized.example.com",
            "login_username": "unauthorizedUser",
            "saved_password": "UnauthorizedPassword",
            "notes": "Unauthorized notes"
        }
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Gets the credential using the correct owner
    original_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the website was not changed
    assert (
        original_credential["website"]
        == "Original Website"
    )

    # Checks that the username was not changed
    assert (
        original_credential["username"]
        == "originalUser"
    )

    # Checks that the password was not changed
    assert decrypt_password(
        original_credential["encrypted_password"]
    ) == "OriginalPassword123"


# Tests that another user cannot delete the credential
def test_other_user_cannot_delete_credential():

    # Creates two fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_test_credential(first_user_id)

    # Creates a Flask test client
    test_client = app.test_client()

    # Logs in as the second user
    log_in_test_user(
        test_client,
        second_user_id,
        "secondUser"
    )

    # Tries to delete the first user's credential
    response = test_client.post(
        "/credentials/" + str(entry_id) + "/delete"
    )

    # Checks that the user was redirected
    assert response.status_code == 302

    # Gets the credential using the correct owner
    original_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the credential still exists
    assert original_credential is not None

    # Checks that its information was not changed
    assert (
        original_credential["website"]
        == "Original Website"
    )
