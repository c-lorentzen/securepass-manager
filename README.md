# SecurePass Manager

SecurePass Manager is a web-based password manager being developed for the CIS2619 SDLC Project Part 3.

The program will allow registered users to securely manage saved credentials for websites and applications.

## Main Features

* User registration
* User login and logout
* Add saved credentials
* View and search saved credentials
* Edit and delete saved credentials
* Account-password hashing
* Saved-password encryption
* User session protection
* Master-password update
* Basic Help documentation

## Technology

* Python
* Flask
* SQLite
* pytest
* HTML
* Basic CSS

## Group Members

* Cristhian Lorentzen — Registration
* Dylan Bloom — Authentication and Sessions
* Elissa Schlosser — Dashboard, Search, and View
* Prerak Patel — Database
* Samantha Lopez Ovalle — Add, Edit, Delete, and Help
* Scott Holznagel — Hashing, Encryption, and Master Password

## Repository Structure

The project will contain the Flask application, HTML templates, CSS files, automated tests, database functions, security functions, and project documentation.

## Branch Workflow

Each group member should work on their assigned branch instead of making changes directly to `main`.

Planned branches:

* `cristhian-registration`
* `dylan-authentication`
* `elissa-dashboard`
* `prerak-database`
* `samantha-credentials`
* `scott-security`

Before beginning work:

1. Open GitHub Desktop.
2. Fetch the latest changes.
3. Switch to your assigned branch.
4. Make and test your changes.
5. Create a clear commit.
6. Push the branch to GitHub.
7. Inform the group when the work is ready for integration.

## Security Rules

Do not upload:

* Real passwords
* Personal information
* Database files containing real information
* Encryption keys
* Secret keys
* Environment-variable files
* Private configuration values

Only fictional test information should be used.

## Testing

Each member is responsible for creating automated tests for their assigned component.

The group will also perform integration testing for this workflow:

Register → Login → Add Credential → Retrieve Credential → Search → View → Edit → Delete → Update Master Password → Logout

The group must also verify that one user cannot access another user’s saved credentials.

## Documentation

Each member is responsible for:

* Their assigned code component
* Unit tests
* Test-result evidence
* A brief explanation of their files and functions
* Their AI-use documentation
* Their personal contribution statement
* Participation in integration testing
* Participation in the final video
