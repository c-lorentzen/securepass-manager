# Registration Component

## Responsible Group Member

Cristhian Lorentzen

## Component Purpose

The Registration component allows a new user to enter a username, email address, password, and confirmation password before creating an account in SecurePass Manager

## Files Created or Updated

* `securepass/registration.py`

  * Contains the `validate_registration()` function
  * Checks parameter types
  * Checks required fields
  * Checks the email format
  * Checks the password requirements
  * Checks that both password values match
  * Checks whether the username or email already exists

* `templates/register.html`

  * Displays the Registration form
  * Displays validation messages
  * Preserves the username and email after an invalid submission
  * Does not preserve password values

* `app.py`

  * Creates the Flask application
  * Displays the Registration page
  * Reads information submitted through the form
  * Sends the form information to the validation function

* `tests/test_registration.py`

  * Tests the Registration validation function

* `tests/test_registration_route.py`

  * Tests the Flask Registration page and form

* `requirements.txt`

  * Includes Flask and pytest

## Validation Rules

The Registration component checks the following requirements:

* The username, email, password, and confirmation password must contain text
* The required fields cannot be empty
* The email must follow a basic email format
* The password must contain at least 8 characters
* The password must contain at least one uppercase letter
* The password must contain at least one lowercase letter
* The password must contain at least one number
* The password and confirmation password must match
* The username cannot already be registered
* The email cannot already be registered

## Automated Test Results

The Registration component currently has 12 automated tests

* 9 tests check the Registration validation function
* 3 tests check the Flask Registration page and form
* All 12 tests passed

Command used:

py -m pytest tests -v


Final result:

12 passed


## Current Integration Status

The Registration form, validation function, duplicate-check logic, Flask route, and automated tests are complete

The duplicate-check logic is prepared to receive database results, but it is not connected to SQLite yet

The account is also not saved yet because the Registration component still needs the database user functions and password-hashing function from the other assigned components

The current success message clearly explains that valid information has not been saved yet
