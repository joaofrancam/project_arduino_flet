
import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def create_user_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(50) UNIQUE NOT NULL,
        senha VARCHAR(50) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def insert_user(login, senha):
    try:
        cursor.execute("INSERT INTO user (login, senha) VALUES (?, ?)", (login, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(login, senha):
    cursor.execute("SELECT id FROM user WHERE login = ? AND senha = ?", (login, senha))
    return cursor.fetchone()

def get_user_id(login):
    cursor.execute("SELECT id FROM user WHERE login = ?", (login,))
    return cursor.fetchone()
