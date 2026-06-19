# Author: Elissa Schlosser
# Course ID and section #: CIS2619.0M1
# Project: SecurePass Manager
# Program description: Creates and displays the user dashboard
# where authenticated users can access and manage their saved credentials.

# Imports the render_template function
from flask import render_template

# Imports the Flask application from app.py
from app import app


# Creates the dashboard route
@app.route("/dashboard")
def dashboard():

    # Displays the dashboard page
    return render_template("dashboard.html")
