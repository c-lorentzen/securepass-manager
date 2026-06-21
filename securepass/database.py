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

# Creates and stores a new credential for one user
def create_credential(
    user_id,
    website,
    website_url,
    login_username,
    encrypted_password,
    notes,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Turns on support for foreign keys
    connection.execute("PRAGMA foreign_keys = ON")

    # Stores the credential using a parameterized query
    cursor = connection.execute(
        """
        INSERT INTO password_entries (
            user_id,
            website,
            website_url,
            login_username,
            encrypted_password,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            website,
            website_url,
            login_username,
            encrypted_password,
            notes
        )
    )

    # Saves the new credential
    connection.commit()

    # Stores the ID created by SQLite
    entry_id = cursor.lastrowid

    # Closes the database connection
    connection.close()

    # Returns the new credential ID
    return entry_id


# Gets every credential that belongs to one user
def get_credentials_by_user(
    user_id,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Gets only the credentials owned by the user
    credential_results = connection.execute(
        """
        SELECT
            entry_id,
            website,
            website_url,
            login_username,
            encrypted_password,
            notes
        FROM password_entries
        WHERE user_id = ?
        ORDER BY website
        """,
        (user_id,)
    ).fetchall()

    # Closes the database connection
    connection.close()

    # Creates an empty list for the credentials
    credentials = []

    # Goes through every database result
    for credential_result in credential_results:

        # Creates a dictionary for the current credential
        credential = {
            "id": credential_result[0],
            "website": credential_result[1],
            "website_url": credential_result[2],
            "username": credential_result[3],
            "encrypted_password": credential_result[4],
            "notes": credential_result[5]
        }

        # Adds the credential to the list
        credentials.append(credential)

    # Returns the user credentials
    return credentials


# Searches credentials that belong to one user
def search_credentials(
    user_id,
    search_term,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Creates the value used by the LIKE query
    search_value = "%" + search_term + "%"

    # Searches only credentials owned by the user
    credential_results = connection.execute(
        """
        SELECT
            entry_id,
            website,
            website_url,
            login_username,
            encrypted_password,
            notes
        FROM password_entries
        WHERE user_id = ?
        AND (
            website LIKE ?
            OR website_url LIKE ?
            OR login_username LIKE ?
            OR notes LIKE ?
        )
        ORDER BY website
        """,
        (
            user_id,
            search_value,
            search_value,
            search_value,
            search_value
        )
    ).fetchall()

    # Closes the database connection
    connection.close()

    # Creates an empty list for the search results
    credentials = []

    # Goes through every search result
    for credential_result in credential_results:

        # Creates a dictionary for the current credential
        credential = {
            "id": credential_result[0],
            "website": credential_result[1],
            "website_url": credential_result[2],
            "username": credential_result[3],
            "encrypted_password": credential_result[4],
            "notes": credential_result[5]
        }

        # Adds the credential to the search results
        credentials.append(credential)

    # Returns the matching credentials
    return credentials


# Gets one credential only when it belongs to the user
def get_credential_by_id(
    entry_id,
    user_id,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Searches using both the entry ID and user ID
    credential_result = connection.execute(
        """
        SELECT
            entry_id,
            website,
            website_url,
            login_username,
            encrypted_password,
            notes
        FROM password_entries
        WHERE entry_id = ?
        AND user_id = ?
        """,
        (
            entry_id,
            user_id
        )
    ).fetchone()

    # Closes the database connection
    connection.close()

    # Returns None when the credential was not found
    if credential_result is None:
        return None

    # Creates a dictionary for the credential
    credential = {
        "id": credential_result[0],
        "website": credential_result[1],
        "website_url": credential_result[2],
        "username": credential_result[3],
        "encrypted_password": credential_result[4],
        "notes": credential_result[5]
    }

    # Returns the credential
    return credential


# Updates one credential only when it belongs to the user
def update_credential(
    entry_id,
    user_id,
    website,
    website_url,
    login_username,
    encrypted_password,
    notes,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Updates the credential using parameterized values
    cursor = connection.execute(
        """
        UPDATE password_entries
        SET
            website = ?,
            website_url = ?,
            login_username = ?,
            encrypted_password = ?,
            notes = ?,
            date_updated = CURRENT_TIMESTAMP
        WHERE entry_id = ?
        AND user_id = ?
        """,
        (
            website,
            website_url,
            login_username,
            encrypted_password,
            notes,
            entry_id,
            user_id
        )
    )

    # Saves the changes
    connection.commit()

    # Checks if one credential was updated
    credential_updated = cursor.rowcount == 1

    # Closes the database connection
    connection.close()

    # Returns the final result
    return credential_updated


# Deletes one credential only when it belongs to the user
def delete_credential(
    entry_id,
    user_id,
    db_path=DATABASE_PATH
):

    # Opens a connection to the database
    connection = sqlite3.connect(db_path)

    # Deletes using both the entry ID and user ID
    cursor = connection.execute(
        """
        DELETE FROM password_entries
        WHERE entry_id = ?
        AND user_id = ?
        """,
        (
            entry_id,
            user_id
        )
    )

    # Saves the deletion
    connection.commit()

    # Checks if one credential was deleted
    credential_deleted = cursor.rowcount == 1

    # Closes the database connection
    connection.close()

    # Returns the final result
    return credential_deleted