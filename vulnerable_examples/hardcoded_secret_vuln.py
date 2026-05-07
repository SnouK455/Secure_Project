"""Educational insecure example: hardcoded secret."""

API_SECRET = "super-secret-prod-key-123456"  # nosec B105


def sign_payload(payload: str) -> str:
    return f"{payload}.{API_SECRET}"
