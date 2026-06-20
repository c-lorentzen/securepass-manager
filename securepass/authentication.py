# securepass/authentication.py
import sqlite3
from werkzeug.security import check_password_hash


class AuthenticationService:
    def __init__(self, db_path="securepass.db"):
        self._db_path = db_path
        self._current_user_id = None  # used for session tests

    # Main authentication method (used by tests)
    def AuthenticateUser(self, username, password):
        if not username or not username.strip():
            return False

        if not password:
            return False

        conn = sqlite3.connect(self._db_path)

        row = conn.execute(
            "SELECT user_id, password_hash FROM users WHERE username = ? OR email = ?",
            (username.strip(), username.strip())
        ).fetchone()

        conn.close()

        if row is None:
            return False

        user_id, password_hash = row
        return check_password_hash(password_hash, password)

    # Lowercase alias (used by app.py)
    def authenticate_user(self, username, password):
        return self.AuthenticateUser(username, password)

    # Session helpers required by your tests
    def CreateSession(self, user_id):
        self._current_user_id = user_id

    def EndSession(self):
        self._current_user_id = None

    def IsUserLoggedIn(self):
        return self._current_user_id is not None
