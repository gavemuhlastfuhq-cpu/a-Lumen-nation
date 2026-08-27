import unittest

from backend.main import app


class BackendRegressionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["app"],
            "Lumen Nation",
        )

        self.assertEqual(
            data["status"],
            "online",
        )

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertTrue(
            data["healthy"]
        )

    def test_users_requires_json_object(self):
        response = self.client.post(
            "/users",
            data="not json",
            content_type="text/plain",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_users_requires_username(self):
        response = self.client.post(
            "/users",
            json={},
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_chat_requires_json_object(self):
        response = self.client.post(
            "/chat",
            data="not json",
            content_type="text/plain",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_chat_requires_message(self):
        response = self.client.post(
            "/chat",
            json={
                "username": "Rocky",
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_history_validates_username(self):
        response = self.client.get(
            "/history/" + ("x" * 101)
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_api_v1_exists(self):
        response = self.client.get(
            "/api/v1/profiles/does-not-exist"
        )

        self.assertEqual(
            response.status_code,
            404,
        )


if __name__ == "__main__":
    unittest.main()
