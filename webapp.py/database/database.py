import sqlite3

# Create or connect to database
conn = sqlite3.connect("users.db")

# Create a cursor (used to execute commands)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

print("Database and table created!")

conn.commit()
conn.close()