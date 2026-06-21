# Author: Dylan Bloom
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: The program verifies Login information using
# the SQLite database and the stored password hash


# Imports the database function used to find a user
from securepass.database import get_user_by_login

# Imports the password verification function
from security_utils import verify_password


# Handles Login validation and user authentication
class AuthenticationService:

    # Creates the Authentication service
    def __init__(self, db_path="securepass.db"):

        # Stores the database path used by the service
        self._db_path = db_path

        # Stores the authenticated user ID
        self._current_user_id = None

    # Checks the username or email and password
    def AuthenticateUser(self, username_or_email, password):

        # Checks if the username or email is text
        if type(username_or_email) != str:
            return False

        # Checks if the password is text
        if type(password) != str:
            return False

        # Removes extra spaces from the Login value
        username_or_email = username_or_email.strip()

        # Checks if the username or email is empty
        if username_or_email == "":
            return False

        # Checks if the password is empty
        if password == "":
            return False

        # Gets the user from the database
        user = get_user_by_login(
            username_or_email,
            self._db_path
        )

        # Returns False when the user does not exist
        if user is None:
            self._current_user_id = None
            return False

        # Stores the password hash from the database result
        stored_password_hash = user[3]

        # Checks the entered password against the stored hash
        password_is_valid = verify_password(
            password,
            stored_password_hash
        )

        # Stores the user ID when the password is correct
        if password_is_valid == True:
            self._current_user_id = user[0]
            return True

        # Removes the current user ID when Authentication fails
        self._current_user_id = None

        # Returns False because the password was incorrect
        return False

    # Provides the lowercase function name used by app.py
    def authenticate_user(self, username_or_email, password):

        # Calls the main Authentication function
        return self.AuthenticateUser(
            username_or_email,
            password
        )

    # Gets the authenticated user ID
    def get_authenticated_user_id(self):

        # Returns the current authenticated user ID
        return self._current_user_id

    # Stores a user ID for the service session tests
    def CreateSession(self, user_id):

        # Stores the provided user ID
        self._current_user_id = user_id

    # Removes the user ID from the service
    def EndSession(self):

        # Clears the stored user ID
        self._current_user_id = None

    # Checks whether the service has a user ID
    def IsUserLoggedIn(self):

        # Returns True when a user ID is stored
        return self._current_user_id is not None