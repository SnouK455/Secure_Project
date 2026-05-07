"""Educational SQL injection example (do not use)."""

import sqlite3


def get_user_by_email_unsafe(email: str) -> list[tuple]:
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    query = f"SELECT id, email FROM users WHERE email = '{email}'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows
