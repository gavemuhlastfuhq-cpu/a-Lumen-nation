import sqlite3

from flask import Blueprint, jsonify, request

from database.connection import get_connection

api_v1 = Blueprint("api_v1", __name__)


def get_db():
    return get_connection()


def error(message, status=400):
    return jsonify({"error": message}), status


def get_user(conn, username):
    return conn.execute(
        """
        SELECT id, username, created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()


def json_body():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None, error(
            "Request body must be a JSON object."
        )

    return data, None


# =========================
# PROFILES
# =========================

@api_v1.route("/profiles/<username>", methods=["GET"])
def get_profile(username):
    conn = get_db()

    user = get_user(conn, username)

    if user is None:
        conn.close()
        return error("User not found.", 404)

    profile = conn.execute(
        """
        SELECT *
        FROM profiles
        WHERE user_id = ?
        """,
        (user["id"],)
    ).fetchone()

    conn.close()

    return jsonify({
        "user": dict(user),
        "profile": dict(profile) if profile else None
    })


@api_v1.route("/profiles", methods=["POST"])
def save_profile():
    data, response = json_body()

    if response:
        return response

    username = data.get("username")

    if not isinstance(username, str) or not username.strip():
        return error("username is required.")

    conn = get_db()
    user = get_user(conn, username.strip())

    if user is None:
        conn.close()
        return error("User not found.", 404)

    conn.execute(
        """
        INSERT INTO profiles (
            user_id,
            display_name,
            bio,
            location
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            display_name = excluded.display_name,
            bio = excluded.bio,
            location = excluded.location,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            user["id"],
            data.get("display_name"),
            data.get("bio"),
            data.get("location")
        )
    )

    conn.commit()

    profile = conn.execute(
        "SELECT * FROM profiles WHERE user_id = ?",
        (user["id"],)
    ).fetchone()

    conn.close()

    return jsonify(dict(profile)), 201


# =========================
# TIMELINE
# =========================

@api_v1.route("/timeline/<username>", methods=["GET"])
def get_timeline(username):
    conn = get_db()

    user = get_user(conn, username)

    if user is None:
        conn.close()
        return error("User not found.", 404)

    rows = conn.execute(
        """
        SELECT *
        FROM timeline
        WHERE user_id = ?
        ORDER BY id
        """,
        (user["id"],)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@api_v1.route("/timeline", methods=["POST"])
def add_timeline():
    data, response = json_body()

    if response:
        return response

    username = data.get("username")
    title = data.get("title")

    if not isinstance(username, str) or not username.strip():
        return error("username is required.")

    if not isinstance(title, str) or not title.strip():
        return error("title is required.")

    conn = get_db()
    user = get_user(conn, username.strip())

    if user is None:
        conn.close()
        return error("User not found.", 404)

    cursor = conn.execute(
        """
        INSERT INTO timeline (
            user_id,
            title,
            description,
            event_date
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user["id"],
            title.strip(),
            data.get("description"),
            data.get("event_date")
        )
    )

    conn.commit()

    row = conn.execute(
        "SELECT * FROM timeline WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(row)), 201


# =========================
# ISSUES
# =========================

@api_v1.route("/issues", methods=["GET"])
def get_issues():
    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            issues.id,
            issues.user_id,
            users.username,
            issues.title,
            issues.description,
            issues.status,
            issues.created_at,
            issues.updated_at
        FROM issues
        JOIN users ON users.id = issues.user_id
        ORDER BY issues.id DESC
        """
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@api_v1.route("/issues", methods=["POST"])
def add_issue():
    data, response = json_body()

    if response:
        return response

    username = data.get("username")
    title = data.get("title")

    if not isinstance(username, str) or not username.strip():
        return error("username is required.")

    if not isinstance(title, str) or not title.strip():
        return error("title is required.")

    conn = get_db()
    user = get_user(conn, username.strip())

    if user is None:
        conn.close()
        return error("User not found.", 404)

    cursor = conn.execute(
        """
        INSERT INTO issues (
            user_id,
            title,
            description,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user["id"],
            title.strip(),
            data.get("description"),
            data.get("status", "open")
        )
    )

    conn.commit()

    row = conn.execute(
        "SELECT * FROM issues WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(row)), 201


# =========================
# RESOURCES
# =========================

@api_v1.route("/resources", methods=["GET"])
def get_resources():
    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            resources.id,
            resources.user_id,
            users.username,
            resources.title,
            resources.description,
            resources.category,
            resources.location,
            resources.status,
            resources.created_at,
            resources.updated_at
        FROM resources
        LEFT JOIN users ON users.id = resources.user_id
        ORDER BY resources.id DESC
        """
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@api_v1.route("/resources", methods=["POST"])
def add_resource():
    data, response = json_body()

    if response:
        return response

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return error("title is required.")

    username = data.get("username")
    user_id = None

    conn = get_db()

    if username:
        user = get_user(conn, username)

        if user is None:
            conn.close()
            return error("User not found.", 404)

        user_id = user["id"]

    cursor = conn.execute(
        """
        INSERT INTO resources (
            user_id,
            title,
            description,
            category,
            location,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title.strip(),
            data.get("description"),
            data.get("category"),
            data.get("location"),
            data.get("status", "available")
        )
    )

    conn.commit()

    row = conn.execute(
        "SELECT * FROM resources WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(row)), 201


# =========================
# CONNECTIONS
# =========================

@api_v1.route("/connections/<username>", methods=["GET"])
def get_connections(username):
    conn = get_db()

    user = get_user(conn, username)

    if user is None:
        conn.close()
        return error("User not found.", 404)

    rows = conn.execute(
        """
        SELECT
            connections.id,
            connections.user_id,
            connections.connected_user_id,
            users.username AS connected_username,
            connections.status,
            connections.created_at
        FROM connections
        JOIN users
            ON users.id = connections.connected_user_id
        WHERE connections.user_id = ?
        ORDER BY connections.id DESC
        """,
        (user["id"],)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@api_v1.route("/connections", methods=["POST"])
def add_connection():
    data, response = json_body()

    if response:
        return response

    username = data.get("username")
    connected_username = data.get("connected_username")

    if not isinstance(username, str) or not username.strip():
        return error("username is required.")

    if not isinstance(connected_username, str) or not connected_username.strip():
        return error("connected_username is required.")

    conn = get_db()

    user = get_user(conn, username.strip())
    connected = get_user(conn, connected_username.strip())

    if user is None or connected is None:
        conn.close()
        return error("One or both users were not found.", 404)

    if user["id"] == connected["id"]:
        conn.close()
        return error("A user cannot connect to themselves.")

    try:
        cursor = conn.execute(
            """
            INSERT INTO connections (
                user_id,
                connected_user_id,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                user["id"],
                connected["id"],
                data.get("status", "pending")
            )
        )

        conn.commit()

    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return error("Connection already exists.", 409)

    row = conn.execute(
        """
        SELECT
            connections.id,
            connections.user_id,
            connections.connected_user_id,
            users.username AS connected_username,
            connections.status,
            connections.created_at
        FROM connections
        JOIN users
            ON users.id = connections.connected_user_id
        WHERE connections.id = ?
        """,
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(row)), 201


# -------------------------
# MATCHING
# -------------------------

from matching.engine import find_matches


@api_v1.route("/issues/<int:issue_id>/matches", methods=["GET"])
def get_issue_matches(issue_id):
    try:
        minimum_score = int(
            request.args.get("minimum_score", 1)
        )
    except ValueError:
        return error(
            "minimum_score must be an integer."
        )

    if minimum_score < 1:
        return error(
            "minimum_score must be at least 1."
        )

    matches = find_matches(
        issue_id,
        minimum_score=minimum_score
    )

    return jsonify({
        "issue_id": issue_id,
        "minimum_score": minimum_score,
        "matches": matches
    })
