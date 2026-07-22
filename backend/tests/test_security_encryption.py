import pytest
from app.core.security import encrypt_credential, decrypt_credential

def test_aes_credential_encryption():
    secret_token = "my_secret_oauth_token_12345!@#"
    encrypted = encrypt_credential(secret_token)
    
    assert encrypted != secret_token
    assert len(encrypted) > 0

    decrypted = decrypt_credential(encrypted)
    assert decrypted == secret_token

def test_empty_string_encryption():
    assert encrypt_credential("") == ""
    assert decrypt_credential("") == ""
