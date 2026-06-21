# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_credentials_database.py
# Program description: The program automatically tests the SQLite
# credential functions used by SecurePass Manager


# Imports the operating system module to remove the test database
import os

# Imports the database setup and user functions
from securepass.database import initialize_database
from securepass.database import create_user
from securepass.database import get_user_by_login

# Imports the credential database functions
from securepass.database import create_credential
from securepass.database import get_credentials_by_user
from securepass.database import search_credentials
from securepass.database import get_credential_by_id
from securepass.database import update_credential
from securepass.database import delete_credential


# Stores the database file used only during automated testing
TEST_DATABASE_PATH = "test_credentials.db"


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

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)


# Removes the database after every test
def teardown_function():

    # Removes the completed test database
    remove_test_database()


# Creates two fictional users and returns their IDs
def create_test_users():

    # Creates the first fictional user
    create_user(
        "firstUser",
        "first@email.com",
        "first_password_hash",
        TEST_DATABASE_PATH
    )

    # Creates the second fictional user
    create_user(
        "secondUser",
        "second@email.com",
        "second_password_hash",
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

    # Stores the first user ID
    first_user_id = first_user[0]

    # Stores the second user ID
    second_user_id = second_user[0]

    # Returns both user IDs
    return first_user_id, second_user_id


# Tests that a credential can be created and listed
def test_create_and_list_credential():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a fictional credential for the first user
    entry_id = create_credential(
        first_user_id,
        "Student Portal",
        "https://student.example.com",
        "studentUser",
        "encrypted_password_value",
        "School account",
        TEST_DATABASE_PATH
    )

    # Gets the first user's credentials
    credentials = get_credentials_by_user(
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that an entry ID was created
    assert entry_id > 0

    # Checks that one credential was returned
    assert len(credentials) == 1

    # Checks the website name
    assert credentials[0]["website"] == "Student Portal"

    # Checks the login username
    assert credentials[0]["username"] == "studentUser"


# Tests that search returns a matching credential
def test_search_credentials_returns_match():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates the first credential
    create_credential(
        first_user_id,
        "Email Account",
        "https://mail.example.com",
        "emailUser",
        "encrypted_email_password",
        "Personal email",
        TEST_DATABASE_PATH
    )

    # Creates the second credential
    create_credential(
        first_user_id,
        "Bank Account",
        "https://bank.example.com",
        "bankUser",
        "encrypted_bank_password",
        "Checking account",
        TEST_DATABASE_PATH
    )

    # Searches for the email credential
    results = search_credentials(
        first_user_id,
        "Email",
        TEST_DATABASE_PATH
    )

    # Checks that one result was returned
    assert len(results) == 1

    # Checks that the matching website was returned
    assert results[0]["website"] == "Email Account"


# Tests that search returns an empty list when there is no match
def test_search_credentials_no_match():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a fictional credential
    create_credential(
        first_user_id,
        "Work Account",
        "https://work.example.com",
        "workUser",
        "encrypted_work_password",
        "Work login",
        TEST_DATABASE_PATH
    )

    # Searches for information that does not exist
    results = search_credentials(
        first_user_id,
        "Unknown Website",
        TEST_DATABASE_PATH
    )

    # Checks that no credential was returned
    assert results == []


# Tests that one credential can be retrieved using its ID
def test_get_credential_by_id():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a fictional credential
    entry_id = create_credential(
        first_user_id,
        "Streaming Account",
        "https://stream.example.com",
        "streamUser",
        "encrypted_stream_password",
        "Entertainment",
        TEST_DATABASE_PATH
    )

    # Gets the credential using the entry ID and owner ID
    credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the credential was found
    assert credential is not None

    # Checks the credential ID
    assert credential["id"] == entry_id

    # Checks the website name
    assert credential["website"] == "Streaming Account"


# Tests that the owner can update a credential
def test_update_credential():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates the original credential
    entry_id = create_credential(
        first_user_id,
        "Old Website",
        "https://old.example.com",
        "oldUser",
        "old_encrypted_password",
        "Old notes",
        TEST_DATABASE_PATH
    )

    # Updates the credential
    update_result = update_credential(
        entry_id,
        first_user_id,
        "Updated Website",
        "https://updated.example.com",
        "updatedUser",
        "updated_encrypted_password",
        "Updated notes",
        TEST_DATABASE_PATH
    )

    # Gets the updated credential
    updated_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the update succeeded
    assert update_result == True

    # Checks the updated website name
    assert updated_credential["website"] == "Updated Website"

    # Checks the updated username
    assert updated_credential["username"] == "updatedUser"


# Tests that the owner can delete a credential
def test_delete_credential():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a fictional credential
    entry_id = create_credential(
        first_user_id,
        "Temporary Account",
        "https://temporary.example.com",
        "temporaryUser",
        "temporary_encrypted_password",
        "Temporary notes",
        TEST_DATABASE_PATH
    )

    # Deletes the credential
    delete_result = delete_credential(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Tries to retrieve the deleted credential
    deleted_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the deletion succeeded
    assert delete_result == True

    # Checks that the credential no longer exists
    assert deleted_credential is None


# Tests that another user cannot access or change the credential
def test_credential_ownership_protection():

    # Creates the fictional users
    first_user_id, second_user_id = create_test_users()

    # Creates a credential owned by the first user
    entry_id = create_credential(
        first_user_id,
        "Private Account",
        "https://private.example.com",
        "privateUser",
        "private_encrypted_password",
        "Private notes",
        TEST_DATABASE_PATH
    )

    # Tries to retrieve the credential using the second user
    unauthorized_credential = get_credential_by_id(
        entry_id,
        second_user_id,
        TEST_DATABASE_PATH
    )

    # Tries to update the credential using the second user
    unauthorized_update = update_credential(
        entry_id,
        second_user_id,
        "Changed Website",
        "https://changed.example.com",
        "changedUser",
        "changed_encrypted_password",
        "Changed notes",
        TEST_DATABASE_PATH
    )

    # Tries to delete the credential using the second user
    unauthorized_delete = delete_credential(
        entry_id,
        second_user_id,
        TEST_DATABASE_PATH
    )

    # Gets the original credential using the correct owner
    original_credential = get_credential_by_id(
        entry_id,
        first_user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the second user could not view the credential
    assert unauthorized_credential is None

    # Checks that the second user could not update the credential
    assert unauthorized_update == False

    # Checks that the second user could not delete the credential
    assert unauthorized_delete == False

    # Checks that the original credential still exists
    assert original_credential is not None

    # Checks that the original website was not changed
    assert original_credential["website"] == "Private Account"