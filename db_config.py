# Database Configuration
import os
import sqlite3

# Define absolute database path relative to this config file
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.db')

def get_db_connection():
    # If running on Vercel, open in read-only mode to prevent write errors on a read-only filesystem
    if os.environ.get('VERCEL') == '1':
        # Open SQLite in read-only mode using URI syntax
        conn = sqlite3.connect(f"file:{DB_FILE}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn
