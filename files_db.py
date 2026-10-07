import sqlite3

DATABASE = "users.db"


def init_files_table():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def add_file(user_id, filename):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "INSERT INTO files (user_id, filename) VALUES (?, ?)",
        (user_id, filename)
    )

    conn.commit()
    conn.close()


def get_user_files(user_id):
    conn = sqlite3.connect(DATABASE)

    files = conn.execute(
        "SELECT filename FROM files WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    conn.close()

    return [file[0] for file in files]


def owns_file(user_id, filename):
    conn = sqlite3.connect(DATABASE)

    result = conn.execute(
        "SELECT id FROM files WHERE user_id = ? AND filename = ?",
        (user_id, filename)
    ).fetchone()

    conn.close()

    return result is not None


def delete_file_record(user_id, filename):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM files WHERE user_id = ? AND filename = ?",
        (user_id, filename)
    )

    conn.commit()
    conn.close()
