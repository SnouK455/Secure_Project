"""Secure SQL query with parameterization."""

import sqlite3


def get_user_by_email_safe(email: str) -> list[tuple]:
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute("SELECT id, email FROM users WHERE email = ?", (email,))
    rows = cur.fetchall()
    conn.close()
    return rows
