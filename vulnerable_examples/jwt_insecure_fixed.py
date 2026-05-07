"""Secure JWT validation example."""

from jose import JWTError, jwt


def decode_token_securely(token: str, secret: str, algorithm: str = "HS256") -> dict:
    try:
        return jwt.decode(token, secret, algorithms=[algorithm], options={"verify_aud": False})
    except JWTError as exc:
        raise ValueError("Invalid JWT token") from exc
