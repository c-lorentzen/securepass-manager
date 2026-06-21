# Author: Dylan Bloom
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_authentication.py
# Program description: The program automatically tests Login
# authentication using SQLite and password hashing


# Imports the operating system module to remove the test database
import os

# Imports the Authentication service
from securepass.authentication import AuthenticationService

# Imports the database functions used during testing
from securepass.database import initialize_database
from securepass.database import create_user

# Imports the password hashing function
from security_utils import hash_password


# Stores the database file used only for Authentication tests
TEST_DATABASE_PATH = "test_authentication.db"


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


# Creates a fresh user database before every test
def setup_function():

    # Removes information left by another test
    remove_test_database()

    # Creates the database tables
    initialize_database(TEST_DATABASE_PATH)

    # Creates a protected hash for the fictional password
    password_hash = hash_password("Password123")

    # Creates a fictional user
    create_user(
        "testUser",
        "test@email.com",
        password_hash,
        TEST_DATABASE_PATH
    )


# Removes the test database after every test
def teardown_function():

    # Removes the completed test database
    remove_test_database()


# Tests Login using a valid username and password
def test_valid_login_with_username():

    # Creates the Authentication service
    auth_service = AuthenticationService(TEST_DATABASE_PATH)

    # Checks the fictional Login information
    actual_result = auth_service.AuthenticateUser(
        "testUser",
        "Password123"
    )

    # Checks that Authentication succeeded
    assert actual_result == True

    # Checks that the real database user ID was stored
    assert auth_service.get_authenticated_user_id() == 1


# Tests Login using a valid email and password
def test_valid_login_with_email():

    # Creates the Authentication service
    auth_service = AuthenticationService(TEST_DATABASE_PATH)

    # Checks the fictional Login information
    actual_result = auth_service.AuthenticateUser(
        "test@email.com",
        "Password123"
    )

    # Checks that Authentication succeeded
    assert actual_result == True


# Tests an incorrect password
def test_wrong_password():

    # Creates the Authentication service
    auth_service = AuthenticationService(TEST_DATABASE_PATH)

    # Tries to log in using an incorrect password
    actual_result = auth_service.AuthenticateUser(
        "testUser",
        "WrongPassword123"
    )

    # Checks that Authentication failed
    assert actual_result == False

    # Checks that no user ID was stored
    assert auth_service.get_authenticated_user_id() is None


# Tests a user that does not exist
def test_unknown_user():

    # Creates the Authentication service
    auth_service = AuthenticationService(TEST_DATABASE_PATH)

    # Tries to log in using an unknown username
    actual_result = auth_service.AuthenticateUser(
        "unknownUser",
        "Password123"
    )

    # Checks that Authentication failed
    assert actual_result == False


# Tests invalid Login parameter types
def test_invalid_login_parameter_types():

    # Creates the Authentication service
    auth_service = AuthenticationService(TEST_DATABASE_PATH)

    # Uses an integer instead of text for the Login value
    username_result = auth_service.AuthenticateUser(
        12345,
        "Password123"
    )

    # Uses None instead of text for the password
    password_result = auth_service.AuthenticateUser(
        "testUser",
        None
    )

    # Checks that both invalid parameter types were rejected
    assert username_result == False
    assert password_result == False