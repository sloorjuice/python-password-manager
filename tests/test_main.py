import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open
from main import ( 
    validate_pw, validate_email, generate_salt, 
    derive_key_from_password, encrypt_password, decrypt_password, generate_pw
)

# PASSWORD VALIDATION

def test_validate_pw_strong():
    assert validate_pw("Str0ngP@ssw0rd!_") == True
    
def test_validate_pw_weak():
    assert validate_pw("weak") == False

def test_validate_pw_empty():
    assert validate_pw("") == False

# EMAIL VALIDATION

def test_validate_email_valid():
    assert validate_email("test@example.com") == True

def test_validate_email_missing_at_symbol():
    assert validate_email("testexample.com") == False

def test_validate_email_missing_domain():
    assert validate_email("test@.com") == False

def test_validate_email_missing_username():
    assert validate_email("@example.com") == False

def test_validate_email_invalid():
    assert validate_email("invalid-email") == False

# PASSWORD GENERATION

def test_generate_pw_length():
    pw = generate_pw()
    assert len(pw) == 16

def test_generate_pw_variety():
    pw = generate_pw()
    assert any(c.islower() for c in pw)
    assert any(c.isupper() for c in pw)
    assert any(c.isdigit() for c in pw)
    assert any(not c.isalnum() for c in pw)

# ENCRYPTION

def test_encrypt_decrypt_roundtrip():
    password = "Test123!@#"
    salt = generate_salt()
    key = derive_key_from_password("masterpw", salt)
    encrypted = encrypt_password(password, key)
    decrypted = decrypt_password(encrypted, key)
    assert decrypted == password
