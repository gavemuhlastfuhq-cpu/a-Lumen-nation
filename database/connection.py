"""
Controlled SQLite connection factory.

This module centralizes connection behavior so the rest of
the application does not each invent its own database policy.
"""

import sqlite3

from config import DATABASE_PATH, DATABASE_TIMEOUT_SECONDS


def get_connection():
    conn = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=DATABASE_TIMEOUT_SECONDS,
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")

    return conn
