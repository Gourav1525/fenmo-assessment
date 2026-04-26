import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            amount INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            idempotency_key TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()