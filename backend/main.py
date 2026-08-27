from flask import Flask, jsonify, request

from config import APP_NAME, APP_VERSION, HOST, PORT, DEBUG
from database.connection import get_connection
from backend.validation import (
    validate_message,
    validate_username,
)

from ai.assistant import process_message


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "app": APP_NAME,
        "status": "online",
        "version": APP_VERSION,
    })


@app.route("/health")
def health():
    return jsonify({
        "healthy": True,
        "app": APP_NAME,
        "version": APP_VERSION,
    })


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    try:
        username = validate_username(
            data.get("username")
        )
    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    conn = get_connection()

    try:
        existing = conn.execute(
            """
            SELECT id, username
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if existing:
            return jsonify({
                "error": "Username already exists.",
                "username": username,
            }), 409

        cursor = conn.execute(
            """
            INSERT INTO users (username)
            VALUES (?)
            """,
            (username,),
        )

        conn.commit()

        return jsonify({
            "message": "User created",
            "username": username,
            "id": cursor.lastrowid,
        }), 201

    finally:
        conn.close()


@app.route("/users", methods=["GET"])
def users():
    conn = get_connection()

    try:
        rows = conn.execute(
            """
            SELECT *
            FROM users
            ORDER BY id ASC
            """
        ).fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:
        conn.close()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    try:
        username = validate_username(
            data.get("username")
        )

        message = validate_message(
            data.get("message")
        )

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    conn = get_connection()

    try:
        user = conn.execute(
            """
            SELECT id, username
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if user is None:
            return jsonify({
                "error": "User not found."
            }), 404

        response = process_message(
            username,
            message,
        )

        conn.execute(
            """
            INSERT INTO messages
            (username, message, response)
            VALUES (?, ?, ?)
            """,
            (
                username,
                message,
                response["response"],
            ),
        )

        conn.commit()

        return jsonify(response)

    finally:
        conn.close()


@app.route("/history/<username>", methods=["GET"])
def history(username):
    try:
        username = validate_username(username)
    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    conn = get_connection()

    try:
        rows = conn.execute(
            """
            SELECT *
            FROM messages
            WHERE username = ?
            ORDER BY id ASC
            """,
            (username,),
        ).fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:
        conn.close()


from backend.api_v1 import api_v1

app.register_blueprint(
    api_v1,
    url_prefix="/api/v1",
)


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
