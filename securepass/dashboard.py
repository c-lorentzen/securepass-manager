# Author: Elissa Schlosser
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: Creates and displays the user dashboard
# where authenticated users can access and manage their saved credentials.

# Imports Flask functions for rendering templates and getting search input
from flask import render_template, request

# Imports Flask-login tools for protecting routes and getting the logged in user
from flask_login import login_required, current_user

# Imports the Flask application from app.py
from app import app

# Imports database functions for retrieving and searching credentials
from securepass.database import (
    get_credentials_by_user,
    search_credentials,
    get_credential_by_id
)

# Creates the dashboard route
@app.route("/dashboard")
@login_required
def dashboard():

    # Get credentials that belong to the logged in user
    credentials = get_credentials_by_user(current_user.id)

    # Displays the dashboard page
    return render_template("dashboard.html", credentials=credentials)

# Creates the search route
@app.route("/search")
@login_required
def search():

    # Gets the search term from the query box
    search_term = request.args.get("query", "")

    # Searches only the logged in users credentials
    results = search_credentials(
        current_user.id,
        search_term
    )

    # Displays the search results page
    return render_template(
        "search.html",
        results=results,
        search_term=search_term
    )

# Creates the view credential route
@app.route("/credentials/<int:credential_id>")
@login_required
def view_credential(credential_id):

    # Gets one credential only if it belongs to the user
    credential = get_credential_by_id(
        credential_id,
        current_user.id
    )

    # Displays the credential detail page
    return render_template(
        "view_credential.html",
        credential=credential
    )














    
