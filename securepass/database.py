# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Component: Database
# Program description: The program creates the SQLite database and
# stores and retrieves SecurePass user information


# Imports the SQLite module included with Python
import sqlite3


# Stores the name of the local database file
DATABASE_PATH = "securepass.db"


# Creates the database tables when they do not already exist
def initialize_database(db_path=DATABASE_PATH):

    # Opens a connection to the SQLite database
    connection = sqlite3.connect(db_path)

    # Creates a cursor used to execute SQL commands
    cursor = connection.cursor()

    # Turns on support for foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Creates the users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            date_created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Creates the password entries table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS password_entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            website_url TEXT,
            login_username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            notes TEXT,
            date_created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            date_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """
    )

    # Saves the table changes
    connection.commit()

    # Closes the database connection
    connection.close()


# Checks if a username is already stored
def username_exists(username, db_path=DATABASE_PATH):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Searches for the username using a parameterized query
    user = connection.execute(
        "SELECT user_id FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    # Closes the database connection
    connection.close()

    # Returns True when the username was found
    return user is not None


# Checks if an email is already stored
def email_exists(email, db_path=DATABASE_PATH):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Searches for the email using a parameterized query
    user = connection.execute(
        "SELECT user_id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    # Closes the database connection
    connection.close()

    # Returns True when the email was found
    return user is not None


# Creates and stores a new user
def create_user(
    username,
    email,
    password_hash,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    try:

        # Stores the user using a parameterized query
        connection.execute(
            """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password_hash
            )
        )

        # Saves the new user
        connection.commit()

        # Stores True because the user was created
        user_created = True

    except sqlite3.IntegrityError:

        # Stores False when the username or email already exists
        user_created = False

    # Closes the database connection
    connection.close()

    # Returns the final result
    return user_created


# Gets a user using a username or email
def get_user_by_login(
    username_or_email,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Searches for the user using a parameterized query
    user = connection.execute(
        """
        SELECT
            user_id,
            username,
            email,
            password_hash
        FROM users
        WHERE username = ? OR email = ?
        """,
        (
            username_or_email,
            username_or_email
        )
    ).fetchone()

    # Closes the database connection
    connection.close()

    # Returns the user information or None
    return user


# Gets a user using the user ID
def get_user_by_id(user_id, db_path=DATABASE_PATH):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Searches for the user using a parameterized query
    user = connection.execute(
        """
        SELECT
            user_id,
            username,
            email,
            password_hash
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    # Closes the database connection
    connection.close()

    # Returns the user information or None
    return user