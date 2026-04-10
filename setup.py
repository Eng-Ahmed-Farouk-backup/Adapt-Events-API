import sqlite3

def setup():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                tags TEXT NOT NULL,
                date TEXT NOT NULL,
                ticket_price INTEGER NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL
            )''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                daily_limit INTEGER NOT NULL,
                requests_today INTEGER NOT NULL DEFAULT 0,
                last_request_date TEXT NOT NULL
            )''')
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup()
