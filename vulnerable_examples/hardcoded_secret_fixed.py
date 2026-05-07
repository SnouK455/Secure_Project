"""Secure variant: secret from environment."""

import os


def sign_payload(payload: str) -> str:
    secret = os.getenv("API_SECRET")
    if not secret:
        raise RuntimeError("API_SECRET is required")
    return f"{payload}.{secret}"
