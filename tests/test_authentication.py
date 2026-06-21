import os
import sqlite3
import tempfile
import time
import pytest
from werkzeug.security import generate_password_hash
from securepass.authentication import AuthenticationService


@pytest.fixture
def db_path():
    # Create a temporary SQLite database file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    # Build the test database schema
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT,
            password_hash TEXT
        )
    """)
    conn.execute(
        "INSERT INTO users (user_id, username, email, password_hash) VALUES (?, ?, ?, ?)",
        (1, "testuser", "test@example.com", generate_password_hash("secret123"))
    )
    conn.commit()
    conn.close()
    time.sleep(0.05)

    # Provide the DB path to the test
    yield path

    # Windows sometimes locks SQLite files — retry delete
    for _ in range(5):
        try:
            os.unlink(path)
            break
        except PermissionError:
            time.sleep(0.1)


def test_valid_login(db_path):
    auth = AuthenticationService(db_path)
    assert auth.AuthenticateUser("testuser", "secret123") is True


def test_wrong_password(db_path):
    auth = AuthenticationService(db_path)
    assert auth.AuthenticateUser("testuser", "wrongpass") is False


def test_unknown_user(db_path):
    auth = AuthenticationService(db_path)
    assert auth.AuthenticateUser("nobody", "secret123") is False
