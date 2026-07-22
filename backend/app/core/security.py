import base64
import hashlib
from cryptography.fernet import Fernet
from app.core.config import settings

def _get_fernet_key() -> bytes:
    key_bytes = settings.JWT_SECRET_KEY.encode("utf-8")
    derived = hashlib.sha256(key_bytes).digest()
    return base64.urlsafe_b64encode(derived)

def encrypt_credential(plain_text: str) -> str:
    if not plain_text:
        return ""
    fernet = Fernet(_get_fernet_key())
    return fernet.encrypt(plain_text.encode("utf-8")).decode("utf-8")

def decrypt_credential(cipher_text: str) -> str:
    if not cipher_text:
        return ""
    fernet = Fernet(_get_fernet_key())
    return fernet.decrypt(cipher_text.encode("utf-8")).decode("utf-8")
