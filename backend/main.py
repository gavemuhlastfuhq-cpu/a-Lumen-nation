from flask import Flask, jsonify, request
import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AI_DIR = os.path.join(BASE_DIR, "ai")
sys.path.append(AI_DIR)

from assistant import process_message

app = Flask(__name__)

DB_PATH = os.path.join(BASE_DIR, "database", "lumen.db")


def get_db():
    return sqlite3.connect(DB_PATH)


@app.route("/")
def home():
    return jsonify({
        "app": "Lumen Nation",
        "status": "online",
        "version": "0.3"
    })


@app.route("/health")
def health():
    return jsonify({
        "healthy": True
    })


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username) VALUES (?)",
        (username,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User created",
        "username": username
    })


@app.route("/users", methods=["GET"])
def users():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    conn.close()

    return jsonify(results)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    username = data.get("username")
    message = data.get("message")

    response = process_message(
        username,
        message
    )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (username, message, response)
        VALUES (?, ?, ?)
        """,
        (
            username,
            message,
            response["response"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify(response)


@app.route("/history/<username>", methods=["GET"])
def history(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM messages WHERE username=?",
        (username,)
    )

    results = cursor.fetchall()

    conn.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )
