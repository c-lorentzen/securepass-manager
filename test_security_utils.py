# Author:      Scott Holznagel
# Date:        2026-06-20
# Class:       Santa Fe College, S26 CIS2619.0M1: DESIGN SOFTWARE
# Assignment:  SDLC Project Part 3
# Description: This tests hashes password

import os
import pytest
from cryptography.fernet import Fernet

from security_utils import (
    hash_password,
    verify_password,
    encrypt_password,
    decrypt_password,
    update_master_password
)


@pytest.fixture(autouse=True)
def set_test_key():
    os.environ["SECUREPASS_KEY"] = Fernet.generate_key().decode()


def test_hash_password_creates_hash():
    password = "MySecurePassword123"
    stored_hash = hash_password(password)

    assert stored_hash != password
    assert isinstance(stored_hash, str)


def test_verify_password_accepts_correct_password():
    password = "MySecurePassword123"
    stored_hash = hash_password(password)

    assert verify_password(password, stored_hash) is True


def test_verify_password_rejects_wrong_password():
    password = "MySecurePassword123"
    stored_hash = hash_password(password)

    assert verify_password("WrongPassword", stored_hash) is False


def test_encrypt_and_decrypt_password():
    saved_password = "WebsitePassword456"

    encrypted = encrypt_password(saved_password)
    decrypted = decrypt_password(encrypted)

    assert encrypted != saved_password
    assert decrypted == saved_password


def test_update_master_password_success():
    old_password = "OldPassword123"
    new_password = "NewPassword456"
    stored_hash = hash_password(old_password)

    new_hash = update_master_password(old_password, stored_hash, new_password)

    assert new_hash is not None
    assert verify_password(new_password, new_hash) is True


def test_update_master_password_fails_with_wrong_current_password():
    old_password = "OldPassword123"
    new_password = "NewPassword456"
    stored_hash = hash_password(old_password)

    result = update_master_password("WrongPassword", stored_hash, new_password)

    assert result is None


def test_hash_password_rejects_non_string():
    with pytest.raises(TypeError):
        hash_password(12345)