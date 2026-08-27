import datetime


from database.connection import get_connection


def get_db():
    return get_connection()


def get_resources():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            title,
            description,
            category,
            location,
            status
        FROM resources
        WHERE status = 'available'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_issues():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            title,
            description,
            status
        FROM issues
        WHERE status != 'closed'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_connections(username):
    conn = get_db()

    rows = conn.execute("""
        SELECT
            users.username,
            connections.status
        FROM connections
        JOIN users
            ON users.id = connections.connected_user_id
        JOIN users AS owner
            ON owner.id = connections.user_id
        WHERE owner.username = ?
        ORDER BY connections.id DESC
    """, (username,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def detect_intent(message):
    text = message.lower().strip()

    resource_words = (
        "resource",
        "resources",
        "available",
        "surplus",
        "materials"
    )

    issue_words = (
        "issue",
        "issues",
        "problem",
        "problems",
        "need",
        "needs",
        "cause",
        "causes"
    )

    connection_words = (
        "connection",
        "connections",
        "connected",
        "network",
        "people"
    )

    if any(word in text for word in resource_words):
        return "resources"

    if any(word in text for word in issue_words):
        return "issues"

    if any(word in text for word in connection_words):
        return "connections"

    return "general"


def format_resources(resources):
    if not resources:
        return "There are currently no available resources."

    lines = [
        f"I found {len(resources)} available resource"
        + ("" if len(resources) == 1 else "s")
        + ":"
    ]

    for resource in resources:
        line = f"- {resource['title']}"

        if resource["category"]:
            line += f" [{resource['category']}]"

        if resource["location"]:
            line += f" — {resource['location']}"

        if resource["description"]:
            line += f": {resource['description']}"

        lines.append(line)

    return "\n".join(lines)


def format_issues(issues):
    if not issues:
        return "There are currently no open issues."

    lines = [
        f"I found {len(issues)} open issue"
        + ("" if len(issues) == 1 else "s")
        + ":"
    ]

    for issue in issues:
        line = f"- {issue['title']}"

        if issue["description"]:
            line += f": {issue['description']}"

        lines.append(line)

    return "\n".join(lines)


def format_connections(connections):
    if not connections:
        return "You currently have no connections."

    lines = [
        f"You have {len(connections)} connection"
        + ("" if len(connections) == 1 else "s")
        + ":"
    ]

    for connection in connections:
        lines.append(
            f"- {connection['username']} "
            f"({connection['status']})"
        )

    return "\n".join(lines)


def generate_response(username, message):
    intent = detect_intent(message)

    if intent == "resources":
        return format_resources(get_resources())

    if intent == "issues":
        return format_issues(get_issues())

    if intent == "connections":
        return format_connections(
            get_connections(username)
        )

    return (
        f"I received your message, {username}. "
        "I can currently help you explore "
        "resources, issues, and connections "
        "within Lumen Nation."
    )


def process_message(username, message):
    timestamp = datetime.datetime.now().isoformat(
        sep=" ",
        timespec="seconds"
    )

    response_text = generate_response(
        username,
        message
    )

    return {
        "user": username,
        "message": message,
        "response": response_text,
        "timestamp": timestamp
    }


if __name__ == "__main__":
    print(
        process_message(
            "Rocky",
            "What resources are available?"
        )
    )
