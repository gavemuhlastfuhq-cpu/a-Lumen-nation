import sqlite3

conn = sqlite3.connect("lumen.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE messages
ADD COLUMN response TEXT
""")

conn.commit()
conn.close()

print("Database updated successfully")
