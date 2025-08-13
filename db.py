import sqlite3

# Create database connection
def get_connection():
    return sqlite3.connect("library.db")

# Create books table if not exists
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Initialize database
init_db()
