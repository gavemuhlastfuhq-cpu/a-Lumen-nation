import unittest
import uuid

from backend.main import app


class APIContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

        suffix = uuid.uuid4().hex[:12]

        cls.username = "contract_a_" + suffix
        cls.connected_username = "contract_b_" + suffix
        cls.missing_username = "contract_missing_" + suffix

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
                    f"Failed to create test user: "
                    f"{username} "
                    f"{response.status_code} "
                    f"{response.get_json()}"
                )

    def assert_json_error(self, response, status):
        self.assertEqual(response.status_code, status)
        self.assertEqual(
            response.content_type,
            "application/json",
        )

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertIn("error", data)
        self.assertIsInstance(data["error"], str)
        self.assertTrue(data["error"].strip())

    # ------------------------------------------------
    # USERS
    # ------------------------------------------------

    def test_users_reject_non_object_json(self):
        response = self.client.post(
            "/users",
            json=["not", "an", "object"],
        )

        self.assert_json_error(response, 400)

    def test_users_reject_missing_username(self):
        response = self.client.post(
            "/users",
            json={},
        )

        self.assert_json_error(response, 400)

    def test_users_reject_blank_username(self):
        response = self.client.post(
            "/users",
            json={"username": "   "},
        )

        self.assert_json_error(response, 400)

    # ------------------------------------------------
    # PROFILES
    # ------------------------------------------------

    def test_profile_rejects_missing_username(self):
        response = self.client.post(
            "/api/v1/profiles",
            json={
                "display_name": "Missing User",
            },
        )

        self.assert_json_error(response, 400)

    def test_profile_rejects_unknown_user(self):
        response = self.client.post(
            "/api/v1/profiles",
            json={
                "username": self.missing_username,
            },
        )

        self.assert_json_error(response, 404)

    def test_profile_get_rejects_unknown_user(self):
        response = self.client.get(
            "/api/v1/profiles/" + self.missing_username
        )

        self.assert_json_error(response, 404)

    # ------------------------------------------------
    # TIMELINE
    # ------------------------------------------------

    def test_timeline_rejects_missing_username(self):
        response = self.client.post(
            "/api/v1/timeline",
            json={
                "title": "Missing User",
            },
        )

        self.assert_json_error(response, 400)

    def test_timeline_rejects_missing_title(self):
        response = self.client.post(
            "/api/v1/timeline",
            json={
                "username": self.username,
            },
        )

        self.assert_json_error(response, 400)

    def test_timeline_rejects_unknown_user(self):
        response = self.client.post(
            "/api/v1/timeline",
            json={
                "username": self.missing_username,
                "title": "Unknown User",
            },
        )

        self.assert_json_error(response, 404)

    def test_timeline_get_rejects_unknown_user(self):
        response = self.client.get(
            "/api/v1/timeline/" + self.missing_username
        )

        self.assert_json_error(response, 404)

    # ------------------------------------------------
    # ISSUES
    # ------------------------------------------------

    def test_issue_rejects_missing_username(self):
        response = self.client.post(
            "/api/v1/issues",
            json={
                "title": "Missing User",
            },
        )

        self.assert_json_error(response, 400)

    def test_issue_rejects_missing_title(self):
        response = self.client.post(
            "/api/v1/issues",
            json={
                "username": self.username,
            },
        )

        self.assert_json_error(response, 400)

    def test_issue_rejects_unknown_user(self):
        response = self.client.post(
            "/api/v1/issues",
            json={
                "username": self.missing_username,
                "title": "Unknown User",
            },
        )

        self.assert_json_error(response, 404)

    # ------------------------------------------------
    # RESOURCES
    # ------------------------------------------------

    def test_resource_rejects_missing_title(self):
        response = self.client.post(
            "/api/v1/resources",
            json={
                "username": self.username,
            },
        )

        self.assert_json_error(response, 400)

    def test_resource_rejects_unknown_user(self):
        response = self.client.post(
            "/api/v1/resources",
            json={
                "username": self.missing_username,
                "title": "Unknown User",
            },
        )

        self.assert_json_error(response, 404)

    def test_resource_allows_anonymous_owner(self):
        response = self.client.post(
            "/api/v1/resources",
            json={
                "title": "Unowned Contract Resource",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertEqual(
            data.get("title"),
            "Unowned Contract Resource",
        )
        self.assertIsNone(data.get("user_id"))

    # ------------------------------------------------
    # CONNECTIONS
    # ------------------------------------------------

    def test_connection_rejects_missing_username(self):
        response = self.client.post(
            "/api/v1/connections",
            json={
                "connected_username":
                    self.connected_username,
            },
        )

        self.assert_json_error(response, 400)

    def test_connection_rejects_missing_connected_username(self):
        response = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
            },
        )

        self.assert_json_error(response, 400)

    def test_connection_rejects_unknown_user(self):
        response = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
                "connected_username":
                    self.missing_username,
            },
        )

        self.assert_json_error(response, 404)

    def test_connection_rejects_self_connection(self):
        response = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
                "connected_username": self.username,
            },
        )

        self.assert_json_error(response, 400)

    def test_duplicate_connection_is_rejected(self):
        first = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
                "connected_username":
                    self.connected_username,
            },
        )

        self.assertEqual(first.status_code, 201)

        second = self.client.post(
            "/api/v1/connections",
            json={
                "username": self.username,
                "connected_username":
                    self.connected_username,
            },
        )

        self.assert_json_error(second, 409)

    def test_connections_get_rejects_unknown_user(self):
        response = self.client.get(
            "/api/v1/connections/" +
            self.missing_username
        )

        self.assert_json_error(response, 404)

    # ------------------------------------------------
    # MATCHING
    # ------------------------------------------------

    def test_matches_reject_non_integer_minimum_score(self):
        response = self.client.get(
            "/api/v1/issues/1/matches"
            "?minimum_score=abc"
        )

        self.assert_json_error(response, 400)

    def test_matches_reject_zero_minimum_score(self):
        response = self.client.get(
            "/api/v1/issues/1/matches"
            "?minimum_score=0"
        )

        self.assert_json_error(response, 400)

    def test_matches_reject_negative_minimum_score(self):
        response = self.client.get(
            "/api/v1/issues/1/matches"
            "?minimum_score=-1"
        )

        self.assert_json_error(response, 400)

    def test_matches_accept_valid_minimum_score(self):
        response = self.client.get(
            "/api/v1/issues/999999/matches"
            "?minimum_score=1"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIsInstance(data, dict)
        self.assertEqual(
            data.get("issue_id"),
            999999,
        )
        self.assertEqual(
            data.get("minimum_score"),
            1,
        )
        self.assertIn("matches", data)
        self.assertIsInstance(
            data["matches"],
            list,
        )


if __name__ == "__main__":
    unittest.main()
