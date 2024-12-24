import sqlite3


DATABASE = 'bot_database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT,
                            role TEXT
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS responses (
                            id INTEGER PRIMARY KEY,
                            trigger TEXT,
                            response TEXT
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            message TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
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