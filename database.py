import sqlite3

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos (
    file_unique_id TEXT PRIMARY KEY,
    name TEXT
)
""")

conn.commit()
conn.close()

print("Database Created")