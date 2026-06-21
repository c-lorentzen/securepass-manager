# Author:      Scott Holznagel
# Date:        2026-06-20
# Class:       Santa Fe College, S26 CIS2619.0M1: DESIGN SOFTWARE
# Assignment:  SDLC Project Part 3
# Description: This hashes password



import base64
import hashlib
import os
from cryptography.fernet import Fernet

# Stores the name of the local encryption key file
KEY_FILE_PATH = "securepass.key"


def hash_password(password):
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return base64.b64encode(salt + password_hash).decode()


def verify_password(password, stored_hash):
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    decoded_hash = base64.b64decode(stored_hash.encode())
    salt = decoded_hash[:16]
    original_hash = decoded_hash[16:]

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return new_hash == original_hash


# Gets or creates the encryption key used for saved credentials
def get_encryption_key():

    # Tries to get the encryption key from the environment
    key = os.environ.get("SECUREPASS_KEY")

    # Returns the environment key when it exists
    if key is not None and key != "":
        return key.encode()

    # Checks if the local key file already exists
    if os.path.exists(KEY_FILE_PATH):

        # Opens the local key file
        key_file = open(KEY_FILE_PATH, "rb")

        # Reads the saved encryption key
        saved_key = key_file.read()

        # Closes the key file
        key_file.close()

        # Returns the saved encryption key
        return saved_key

    # Creates a new encryption key
    new_key = Fernet.generate_key()

    # Creates the local key file
    key_file = open(KEY_FILE_PATH, "wb")

    # Saves the new encryption key
    key_file.write(new_key)

    # Closes the key file
    key_file.close()

    # Returns the new encryption key
    return new_key


def encrypt_password(saved_password):
    if not isinstance(saved_password, str):
        raise TypeError("Saved password must be a string.")

    fernet = Fernet(get_encryption_key())
    return fernet.encrypt(saved_password.encode()).decode()


def decrypt_password(encrypted_password):
    if not isinstance(encrypted_password, str):
        raise TypeError("Encrypted password must be a string.")

    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(encrypted_password.encode()).decode()


def update_master_password(current_password, stored_hash, new_password):
    if verify_password(current_password, stored_hash):
        return hash_password(new_password)

    return None