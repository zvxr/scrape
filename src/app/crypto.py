from uuid import UUID

from cryptography.fernet import Fernet

from src.app.models.documents import EncryptionEnum
from src.app.settings import get_settings


def _decrypt_fernet(data: bytes):
    settings = get_settings()
    f = Fernet(settings.fetcher_fernet_secret)
    return f.decrypt(data)


def _encrypt_fernet(data: bytes):
    settings = get_settings()
    f = Fernet(settings.fetcher_fernet_secret)
    return f.encrypt(data)


def decrypt(data: bytes, encryption: UUID):
    if encryption == EncryptionEnum.fernet:
        return _decrypt_fernet(data)


def encrypt(data: bytes, encryption: UUID):
    if encryption == EncryptionEnum.fernet:
        return _encrypt_fernet(data)
