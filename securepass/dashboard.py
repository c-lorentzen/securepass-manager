
# Imports the render_template function
from flask import render_template

# Imports the Flask application from app.py
from app import app


# Creates the dashboard route
@app.route("/dashboard")
def dashboard():

    # Displays the dashboard page
    return render_template("dashboard.html")
