
import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def create_speed_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS speed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        speed INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        id_user INTEGER,
        FOREIGN KEY(id_user) REFERENCES user(id)
    )
    """)
    conn.commit()

def insert_speed(speed_value, user_id):
    cursor.execute("INSERT INTO speed (speed, id_user) VALUES (?, ?)", (speed_value, user_id))
    conn.commit()

def get_user_speeds(login):
    cursor.execute("""
        SELECT speed, speed.created_at FROM speed
        JOIN user ON user.id = speed.id_user
        WHERE user.login = ?
        ORDER BY speed.created_at DESC
    """, (login,))
    return cursor.fetchall()
