"""Educational insecure JWT usage."""

from jose import jwt


def decode_token_without_verification(token: str) -> dict:
    return jwt.get_unverified_claims(token)
