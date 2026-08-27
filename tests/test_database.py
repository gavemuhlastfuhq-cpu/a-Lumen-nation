import unittest

from config import DATABASE_PATH
from database.connection import get_connection


class DatabaseRegressionTests(unittest.TestCase):

    def test_database_path_exists(self):
        self.assertTrue(
            DATABASE_PATH.exists(),
            f"Database does not exist: {DATABASE_PATH}",
        )

    def test_connection_enables_foreign_keys(self):
        conn = get_connection()

        try:
            value = conn.execute(
                "PRAGMA foreign_keys"
            ).fetchone()[0]

            self.assertEqual(value, 1)
        finally:
            conn.close()

    def test_busy_timeout(self):
        conn = get_connection()

        try:
            value = conn.execute(
                "PRAGMA busy_timeout"
            ).fetchone()[0]

            self.assertEqual(value, 5000)
        finally:
            conn.close()

    def test_database_integrity(self):
        conn = get_connection()

        try:
            result = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            self.assertEqual(result, "ok")
        finally:
            conn.close()

    def test_foreign_key_integrity(self):
        conn = get_connection()

        try:
            rows = conn.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

            self.assertEqual(rows, [])
        finally:
            conn.close()

    def test_users_table_exists(self):
        conn = get_connection()

        try:
            row = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'users'
            """).fetchone()

            self.assertIsNotNone(row)
        finally:
            conn.close()

    def test_messages_table_exists(self):
        conn = get_connection()

        try:
            row = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'messages'
            """).fetchone()

            self.assertIsNotNone(row)
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
