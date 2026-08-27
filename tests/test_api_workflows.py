import unittest
import uuid

from backend.main import app


class APIWorkflowTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

        suffix = uuid.uuid4().hex[:12]

        cls.username = "stage6_a_" + suffix
        cls.connected_username = "stage6_b_" + suffix

        # Create prerequisite users once before any workflow test runs.
        for username in (
            cls.username,
            cls.connected_username,
        ):
            response = cls.client.post(
                "/users",
                json={"username": username},
            )

            if response.status_code != 201:
                raise RuntimeError(
                    f"Failed to create test user {username}: "
                    f"{response.status_code} {response.get_json()}"
                )

    def test_health_contract(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertTrue(data.get("healthy"))
        self.assertIn("app", data)
        self.assertIn("version", data)

    def test_create_and_read_users(self):
        response = self.client.get("/users")

        self.assertEqual(response.status_code, 200)

        users = response.get_json()

        self.assertIsInstance(users, list)

        usernames = [
            user["username"]
            for user in users
        ]

        self.assertIn(self.username, usernames)
        self.assertIn(self.connected_username, usernames)

    def test_duplicate_user_is_rejected(self):
        response = self.client.post(
            "/users",
            json={
                "username": self.username,
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_profile_workflow(self):
        response = self.client.post(
            "/api/v1/profiles",
            json={
                "username": self.username,
                "display_name": "Stage 6 Test",
                "bio": "API workflow test",
                "location": "Test Location",
            },
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            "/api/v1/profiles/" + self.username
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertEqual(
            data["user"]["username"],
            self.username,
        )

    def test_timeline_workflow(self):
        response = self.client.post(
            "/api/v1/timeline",
            json={
                "username": self.username,
                "title": "Stage 6 Test Event",
                "description": "Workflow verification",
                "event_date": "2026-08-27",
            },
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            "/api/v1/timeline/" + self.username
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, list)

        self.assertTrue(
            any(
                item.get("title") == "Stage 6 Test Event"
                for item in data
            )
        )

    def test_issue_workflow(self):
        response = self.client.post(
            "/api/v1/issues",
            json={
                "username": self.username,
                "title": "Stage 6 Test Issue",
                "description": "Workflow verification",
            },
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v1/issues")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, list)

        self.assertTrue(
            any(
                item.get("title") == "Stage 6 Test Issue"
                for item in data
            )
        )

    def test_resource_workflow(self):
        response = self.client.post(
            "/api/v1/resources",
            json={
                "username": self.username,
                "title": "Stage 6 Test Resource",
                "description": "Workflow verification",
                "category": "test",
                "location": "Test Location",
            },
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v1/resources")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, list)

        self.assertTrue(
            any(
                item.get("title") == "Stage 6 Test Resource"
                for item in data
            )
        )

    def test_connection_workflow(self):
        response = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
                "connected_username": self.connected_username,
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(
            data["connected_username"],
            self.connected_username,
        )

        response = self.client.get(
            "/api/v1/connections/" + self.username
        )

        self.assertEqual(response.status_code, 200)

        connections = response.get_json()

        self.assertIsInstance(connections, list)

        self.assertTrue(
            any(
                item.get("connected_username")
                == self.connected_username
                for item in connections
            )
        )

    def test_chat_workflow(self):
        response = self.client.post(
            "/chat",
            json={
                "username": self.username,
                "message": "Stage 6 integration test",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertIn("response", data)

        response = self.client.get(
            "/history/" + self.username
        )

        self.assertEqual(response.status_code, 200)

        history = response.get_json()

        self.assertIsInstance(history, list)

        self.assertTrue(
            any(
                item.get("message")
                == "Stage 6 integration test"
                for item in history
            )
        )


if __name__ == "__main__":
    unittest.main()
