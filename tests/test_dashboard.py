# Author: Elissa Schlosser
# Integrated by: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: Tests the Dashboard, Search, and View Credential
# routes used by the integrated SecurePass Manager application


# Imports Path to inspect the credential template
from pathlib import Path

# Imports the Flask application
from app import app


# Gets all route paths registered by the Flask application
def get_application_routes():

    # Creates an empty list for the route paths
    route_paths = []

    # Goes through every Flask route
    for route in app.url_map.iter_rules():

        # Adds the current route path to the list
        route_paths.append(route.rule)

    # Returns all registered route paths
    return route_paths


# Tests that the Dashboard route exists and requires Login
def test_dashboard_route_exists():

    # Gets the registered application routes
    route_paths = get_application_routes()

    # Checks that the Dashboard route exists
    assert "/dashboard" in route_paths

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open the protected Dashboard
    response = test_client.get("/dashboard")

    # Checks that the logged-out user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that the Search route exists and requires Login
def test_search_route_exists():

    # Gets the registered application routes
    route_paths = get_application_routes()

    # Checks that the Search route exists
    assert "/search" in route_paths

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to search while logged out
    response = test_client.get("/search?query=gmail")

    # Checks that the logged-out user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that the View Credential route exists and requires Login
def test_view_credential_route_exists():

    # Gets the registered application routes
    route_paths = get_application_routes()

    # Checks that the View Credential route exists
    assert "/credentials/<int:credential_id>" in route_paths

    # Creates a Flask test client
    test_client = app.test_client()

    # Tries to open a credential while logged out
    response = test_client.get("/credentials/1")

    # Checks that the logged-out user was redirected
    assert response.status_code == 302

    # Checks that the redirect goes to Login
    assert "/login" in response.location


# Tests that the credential password is hidden by default
def test_password_hidden_by_default():

    # Finds the main project folder
    project_path = Path(__file__).resolve().parents[1]

    # Finds the View Credential template
    template_path = (
        project_path
        / "templates"
        / "view_credential.html"
    )

    # Reads the template content
    template_content = template_path.read_text(
        encoding="utf-8"
    )

    # Checks that the password field is hidden by default
    assert 'type="password"' in template_content

    # Checks that the user can choose to show the password
    assert "Show Password" in template_content