"""Primitivas de la biblioteca estándar; nunca registrar contraseñas/tokens."""

import hashlib
import hmac
import secrets
from backend.app.resource_limits import HEAVY_WORK_SLOT

SCRYPT_N = 2**17
SCRYPT_R = 8
SCRYPT_P = 1



def _derive(password: str, salt: bytes) -> bytes:
    with HEAVY_WORK_SLOT:
        return hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R,
            p=SCRYPT_P, maxmem=256 * 1024 * 1024, dklen=32,
        )


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${_derive(password, salt).hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, n, r, p, salt_hex, digest_hex = encoded.split("$")
        if (algorithm, int(n), int(r), int(p)) != ("scrypt", SCRYPT_N, SCRYPT_R, SCRYPT_P):
            return False
        salt, digest = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
        if len(salt) != 16 or len(digest) != 32:
            return False
        return hmac.compare_digest(_derive(password, salt), digest)
    except (ValueError, TypeError):
        return False


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


DUMMY_PASSWORD_HASH = hash_password(secrets.token_urlsafe(32))
