from __future__ import annotations

import hashlib
import os
import secrets


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return digest, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    digest, _ = hash_password(password=password, salt=salt)
    return secrets.compare_digest(digest, password_hash)


def bootstrap_admin_password() -> str:
    return os.getenv("LEXERA_ADMIN_PASSWORD", "Admin@12345")
