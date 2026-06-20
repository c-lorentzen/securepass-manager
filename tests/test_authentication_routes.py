import pytest
from app import app

# Login page loads correctly


def test_login_page_loads_correctly():
    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

# Session is created after successful login (DB-dependent)


@pytest.mark.skip(reason="Database not ready for real login test")
def test_session_created_after_successful_login():
    client = app.test_client()
    response = client.post("/login", data={
        "username": "testuser",
        "password": "correctpassword"
    }, follow_redirects=True)

    assert b"dashboard" in response.data.lower()

# Unauthenticated user cannot access a protected page


def test_unauthenticated_user_blocked_from_protected_page():
    client = app.test_client()
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Login" in response.data

# Authenticated user can access a protected page (DB-dependent)


@pytest.mark.skip(reason="Database not ready for authenticated access test")
def test_authenticated_user_can_access_protected_page():
    client = app.test_client()

    # Fake login once DB is ready
    client.post("/login", data={
        "username": "testuser",
        "password": "correctpassword"
    })

    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Logout removes the user session


def test_logout_removes_user_session():
    client = app.test_client()

    # Create a fake session
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "testuser"

    client.get("/logout", follow_redirects=True)

    # After logout, dashboard should redirect to login
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Login" in response.data
