# Author: Cristhian Lorentzen
# Course ID and section #: CIS2619.0M1
# Date created: 6/19/2026
# Program title: test_registration.py
# Program description: The program automatically tests valid and
# invalid registration information


# Imports the registration validation function that will be tested
from securepass.registration import validate_registration


# Tests registration information that should be completely valid
def test_valid_registration():

    # Stores the username used for the test
    username = "studentUser"

    # Stores the email used for the test
    email = "student@email.com"

    # Stores the password used for the test
    password = "Password123"

    # Stores the matching confirmation password
    confirm_password = "Password123"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = True

    # Creates the expected empty list of error messages
    expected_messages = []

    # Checks that the actual Boolean result matches the expected result
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that no error messages were returned
    assert actual_result["messages"] == expected_messages


# Tests an email that does not have a valid format
def test_invalid_email_format():

    # Stores the username used for the test
    username = "studentUser"

    # Stores an email without the @ symbol
    email = "studentemail.com"

    # Stores a valid password
    password = "Password123"

    # Stores the matching confirmation password
    confirm_password = "Password123"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected list of error messages
    expected_messages = [
        "Please enter a valid email address."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the correct email error message was returned
    assert actual_result["messages"] == expected_messages


# Tests a password that does not follow the password rules
def test_weak_password():

    # Stores the username used for the test
    username = "studentUser"

    # Stores a valid email
    email = "student@email.com"

    # Stores a password that is too short and has limited character types
    password = "pass"

    # Stores the matching confirmation password
    confirm_password = "pass"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected list of password error messages
    expected_messages = [
        "Password must be at least 8 characters long.",
        "Password must contain at least one uppercase letter.",
        "Password must contain at least one number."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the expected password errors were returned
    assert actual_result["messages"] == expected_messages


# Tests passwords that contain different values
def test_passwords_do_not_match():

    # Stores the username used for the test
    username = "studentUser"

    # Stores a valid email
    email = "student@email.com"

    # Stores the original password
    password = "PaSsword123"

    # Stores a different confirmation password
    confirm_password = "PasSword456"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected list of error messages
    expected_messages = [
        "Passwords do not match."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the password matching error was returned
    assert actual_result["messages"] == expected_messages


# Tests an integer used as the username parameter
def test_invalid_username_parameter_type():

    # Stores an integer instead of a string for the username
    username = 12345

    # Stores a valid email
    email = "student@email.com"

    # Stores a valid password
    password = "PassWord123"

    # Stores the matching confirmation password
    confirm_password = "PassWord123"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected parameter type error message
    expected_messages = [
        "Username must be text."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the username type error was returned
    assert actual_result["messages"] == expected_messages


# Tests None used as the email parameter
def test_invalid_email_parameter_type():

    # Stores a valid username
    username = "studentUser"

    # Stores None instead of a string for the email
    email = None

    # Stores a valid password
    password = "PaSsworD123"

    # Stores the matching confirmation password
    confirm_password = "PaSsworD123"

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected parameter type error message
    expected_messages = [
        "Email must be text."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the email type error was returned
    assert actual_result["messages"] == expected_messages


# Tests all required fields with empty string values
def test_empty_registration_fields():

    # Stores an empty username
    username = ""

    # Stores an empty email
    email = ""

    # Stores an empty password
    password = ""

    # Stores an empty confirmation password
    confirm_password = ""

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected list of empty field error messages
    expected_messages = [
        "Please enter a username.",
        "Please enter an email address.",
        "Please enter a password.",
        "Please confirm your password."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that all required field messages were returned
    assert actual_result["messages"] == expected_messages


# Tests a username that is already registered
def test_duplicate_username():

    # Stores valid registration information
    username = "studentUser"
    email = "student@email.com"
    password = "Password123"
    confirm_password = "Password123"

    # Stores True because the username already exists
    username_exists = True

    # Stores False because the email does not already exist
    email_exists = False

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password,
        username_exists,
        email_exists
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected duplicate username message
    expected_messages = [
        "Username is already registered."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the duplicate username message was returned
    assert actual_result["messages"] == expected_messages


# Tests an email that is already registered
def test_duplicate_email():

    # Stores valid registration information
    username = "studentUser"
    email = "student@email.com"
    password = "Password123"
    confirm_password = "Password123"

    # Stores False because the username does not already exist
    username_exists = False

    # Stores True because the email already exists
    email_exists = True

    # Calls the function and stores the actual result
    actual_result = validate_registration(
        username,
        email,
        password,
        confirm_password,
        username_exists,
        email_exists
    )

    # Stores the expected Boolean result
    expected_is_valid = False

    # Creates the expected duplicate email message
    expected_messages = [
        "Email is already registered."
    ]

    # Checks that the registration was marked as invalid
    assert actual_result["is_valid"] == expected_is_valid

    # Checks that the duplicate email message was returned
    assert actual_result["messages"] == expected_messages