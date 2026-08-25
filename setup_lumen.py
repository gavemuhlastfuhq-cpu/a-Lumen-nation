import os

folders = [
    "app",
    "backend",
    "ai",
    "database",
    "security",
    "maps",
    "messaging",
    "resources",
    "docs"
]

files = {
    "backend/main.py": '''from fastapi import FastAPI

app = FastAPI(title="Lumen Nation")

@app.get("/")
def home():
    return {"status": "Lumen Nation is running"}
''',

    "ai/assistant.py": '''def reply(message):
    return f"You said: {message}"
''',

    "database/database.py": '''import sqlite3

conn = sqlite3.connect("database/lumen.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    created TEXT
)
""")

conn.commit()
conn.close()
'''
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("Lumen Nation project created.")
