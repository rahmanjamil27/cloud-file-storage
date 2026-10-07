import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect(DATABASE)

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect(DATABASE)

    user = conn.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):
        return user[0], user[1]

    return None
