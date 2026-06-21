# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/21/2026
# Program title: test_database.py
# Program description: The program automatically tests the SQLite
# database functions used by SecurePass Manager


# Imports the operating system module to remove the test database
import os

# Imports SQLite to check the database tables
import sqlite3

# Imports the database functions that will be tested
from securepass.database import initialize_database
from securepass.database import username_exists
from securepass.database import email_exists
from securepass.database import create_user
from securepass.database import get_user_by_login
from securepass.database import get_user_by_id


# Stores the file used only during automated testing
TEST_DATABASE_PATH = "test_securepass.db"


# Removes the test database when it exists
def remove_test_database():

    # Checks if the main test database exists
    if os.path.exists(TEST_DATABASE_PATH):

        # Removes the main test database
        os.remove(TEST_DATABASE_PATH)

    # Stores the possible SQLite journal file name
    journal_path = TEST_DATABASE_PATH + "-journal"

    # Checks if the test journal file exists
    if os.path.exists(journal_path):

        # Removes the test journal file
        os.remove(journal_path)


# Creates a fresh database before every test
def setup_function():

    # Removes information left by an earlier test
    remove_test_database()

    # Creates a new empty test database
    initialize_database(TEST_DATABASE_PATH)


# Removes the database after every test
def teardown_function():

    # Removes the completed test database
    remove_test_database()


# Tests that the required database tables are created
def test_initialize_database_creates_tables():

    # Opens the test database
    connection = sqlite3.connect(TEST_DATABASE_PATH)

    # Gets the names of the tables from SQLite
    table_results = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    # Closes the test database connection
    connection.close()

    # Creates an empty list to store the table names
    table_names = []

    # Goes through every table result
    for table_result in table_results:

        # Adds the table name to the list
        table_names.append(table_result[0])

    # Checks that the users table was created
    assert "users" in table_names

    # Checks that the password entries table was created
    assert "password_entries" in table_names


# Tests that a user can be created and retrieved
def test_create_and_get_user():

    # Stores a fictional password hash for the database test
    password_hash = "fictional_password_hash"

    # Creates the fictional user
    user_created = create_user(
        "studentUser",
        "student@email.com",
        password_hash,
        TEST_DATABASE_PATH
    )

    # Gets the user using the username
    user = get_user_by_login(
        "studentUser",
        TEST_DATABASE_PATH
    )

    # Checks that the user was created
    assert user_created == True

    # Checks that the user was found
    assert user is not None

    # Checks the stored username
    assert user[1] == "studentUser"

    # Checks the stored email
    assert user[2] == "student@email.com"

    # Checks the stored password hash
    assert user[3] == password_hash


# Tests that the username and email existence checks work
def test_username_and_email_exist():

    # Creates a fictional user
    create_user(
        "existingUser",
        "existing@email.com",
        "fictional_password_hash",
        TEST_DATABASE_PATH
    )

    # Checks the stored username
    username_result = username_exists(
        "existingUser",
        TEST_DATABASE_PATH
    )

    # Checks the stored email
    email_result = email_exists(
        "existing@email.com",
        TEST_DATABASE_PATH
    )

    # Checks that the username was found
    assert username_result == True

    # Checks that the email was found
    assert email_result == True


# Tests that an unknown username and email are not found
def test_unknown_username_and_email():

    # Searches for a username that does not exist
    username_result = username_exists(
        "unknownUser",
        TEST_DATABASE_PATH
    )

    # Searches for an email that does not exist
    email_result = email_exists(
        "unknown@email.com",
        TEST_DATABASE_PATH
    )

    # Checks that the username was not found
    assert username_result == False

    # Checks that the email was not found
    assert email_result == False


# Tests that a duplicate username is rejected
def test_duplicate_username_is_rejected():

    # Creates the first user
    create_user(
        "duplicateUser",
        "first@email.com",
        "first_hash",
        TEST_DATABASE_PATH
    )

    # Tries to create another user with the same username
    second_result = create_user(
        "duplicateUser",
        "second@email.com",
        "second_hash",
        TEST_DATABASE_PATH
    )

    # Checks that the duplicate username was rejected
    assert second_result == False


# Tests that a duplicate email is rejected
def test_duplicate_email_is_rejected():

    # Creates the first user
    create_user(
        "firstUser",
        "duplicate@email.com",
        "first_hash",
        TEST_DATABASE_PATH
    )

    # Tries to create another user with the same email
    second_result = create_user(
        "secondUser",
        "duplicate@email.com",
        "second_hash",
        TEST_DATABASE_PATH
    )

    # Checks that the duplicate email was rejected
    assert second_result == False


# Tests that a user can be found using the user ID
def test_get_user_by_id():

    # Creates a fictional user
    create_user(
        "idUser",
        "iduser@email.com",
        "fictional_password_hash",
        TEST_DATABASE_PATH
    )

    # Gets the user using the username
    login_user = get_user_by_login(
        "idUser",
        TEST_DATABASE_PATH
    )

    # Stores the user ID
    user_id = login_user[0]

    # Gets the same user using the user ID
    id_user = get_user_by_id(
        user_id,
        TEST_DATABASE_PATH
    )

    # Checks that the user was found
    assert id_user is not None

    # Checks that the correct username was returned
    assert id_user[1] == "idUser"

    # Checks that the correct email was returned
    assert id_user[2] == "iduser@email.com"