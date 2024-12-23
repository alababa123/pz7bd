import sqlite3

def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        message TEXT,
        command TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_message(user_id, username, message, command, date):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (user_id, username, message, command, date)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, message, command, date))
    conn.commit()
    conn.close()

def fetch_statistics():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    # Статистика по дням
    cursor.execute("SELECT date, COUNT(*) FROM messages GROUP BY date")
    daily_stats = cursor.fetchall()

    # Статистика по пользователям
    cursor.execute("SELECT username, COUNT(*) FROM messages GROUP BY username")
    user_stats = cursor.fetchall()

    # Статистика по командам
    cursor.execute("SELECT command, COUNT(*) FROM messages WHERE command IS NOT NULL GROUP BY command")
    command_stats = cursor.fetchall()

    conn.close()
    return {"daily": daily_stats, "users": user_stats, "commands": command_stats}