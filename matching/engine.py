import os
import re
import sqlite3


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "lumen.db"
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def tokenize(text):
    if not text:
        return set()

    return set(
        re.findall(
            r"[a-z0-9]+",
            text.lower()
        )
    )


def score_match(issue, resource):
    issue_text = " ".join([
        issue["title"] or "",
        issue["description"] or ""
    ])

    resource_text = " ".join([
        resource["title"] or "",
        resource["description"] or "",
        resource["category"] or ""
    ])

    issue_words = tokenize(issue_text)
    resource_words = tokenize(resource_text)

    if not issue_words or not resource_words:
        return 0

    overlap = issue_words & resource_words

    score = len(overlap)

    if (
        issue.get("location")
        and resource.get("location")
        and issue["location"].lower()
        == resource["location"].lower()
    ):
        score += 2

    return score


def find_matches(issue_id, minimum_score=1):
    conn = get_db()

    issue = conn.execute("""
        SELECT
            id,
            user_id,
            title,
            description,
            status
        FROM issues
        WHERE id = ?
    """, (issue_id,)).fetchone()

    if issue is None:
        conn.close()
        return []

    resources = conn.execute("""
        SELECT
            id,
            user_id,
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

    issue = dict(issue)

    results = []

    for resource in resources:
        resource = dict(resource)

        score = score_match(
            issue,
            resource
        )

        if score >= minimum_score:
            results.append({
                "resource": resource,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results


if __name__ == "__main__":
    matches = find_matches(1)

    print("=== MATCHES ===")

    for match in matches:
        resource = match["resource"]

        print(
            f"{match['score']} | "
            f"{resource['title']}"
        )
