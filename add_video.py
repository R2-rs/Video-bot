import sqlite3

uid = input("Video ID: ")
name = input("Video Name: ")

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO videos (file_unique_id, name) VALUES (?, ?)",
    (uid, name)
)

conn.commit()
conn.close()

print("Saved!")