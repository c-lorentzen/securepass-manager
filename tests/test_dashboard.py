# Author: Elissa Schlosser
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: Tests the dashboard, search, and view credential
# functionality of the SecurePass Manager application.


# Tests that the dashboard route exists and can be accessed
def test_dashboard_route_exists(client):

    # Sends a request to the dashboard page
    response = client.get("/dashboard")

    # Verifies that the page loads or redirects to login
    assert response.status_code in [200, 302]


# Tests that the search route exists and accepts a search query
def test_search_route_exists(client):

    # Sends a search request
    response = client.get("/search?query=gmail")

    # Verifies that the page loads or redirects to login
    assert response.status_code in [200, 302]


# Tests that the view credential route exists
def test_view_credential_route_exists(client):

    # Requests a credential with an example ID
    response = client.get("/credentials/1")

    # Verifies that the page loads or redirects to login
    assert response.status_code in [200, 302]


# Tests that passwords are hidden by default
def test_password_hidden_by_default(client):

    # Requests a credential page
    response = client.get("/credentials/1")

    # Verifies that the hidden password mask is displayed
    assert b"**********" in response.data
