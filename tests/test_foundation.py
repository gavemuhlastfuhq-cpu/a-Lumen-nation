import unittest

from counsel import (
    counsel_count,
    is_odd_counsel_count,
    validate_counsel,
)

from evidence import (
    EvidenceItem,
    EvidenceStatus,
    EpistemicType,
)

from security import (
    DataClass,
    can_collect,
    should_disclose,
)

from security.crisis import (
    CrisisLevel,
    response_requirements,
)

from backend.validation import (
    validate_message,
    validate_username,
)


class FoundationTests(unittest.TestCase):

    def test_counsel_is_odd(self):
        validate_counsel()
        self.assertTrue(is_odd_counsel_count())
        self.assertEqual(counsel_count() % 2, 1)

    def test_evidence_validation(self):
        item = EvidenceItem(
            id="test-1",
            kind=EpistemicType.CLAIM,
            content="Test claim",
            status=EvidenceStatus.UNASSESSED,
            confidence=0.5,
        )

        item.validate()

    def test_invalid_confidence(self):
        item = EvidenceItem(
            id="test-2",
            kind=EpistemicType.CLAIM,
            content="Test claim",
            confidence=2.0,
        )

        with self.assertRaises(ValueError):
            item.validate()

    def test_private_data_requires_purpose(self):
        self.assertFalse(
            can_collect(
                DataClass.PRIVATE,
                "",
            )
        )

        self.assertTrue(
            can_collect(
                DataClass.PRIVATE,
                "user-requested profile storage",
            )
        )

    def test_private_data_defaults_to_no_disclosure(self):
        self.assertFalse(
            should_disclose(
                DataClass.PRIVATE
            )
        )

    def test_user_requested_private_data(self):
        self.assertTrue(
            should_disclose(
                DataClass.PRIVATE,
                user_requested=True,
            )
        )

    def test_crisis_policy(self):
        result = response_requirements(
            CrisisLevel.IMMINENT_DANGER
        )

        self.assertTrue(
            result["human_contact_recommended"]
        )

        self.assertTrue(
            result["emergency_guidance"]
        )

    def test_username_validation(self):
        self.assertEqual(
            validate_username(" Rocky "),
            "Rocky",
        )

        with self.assertRaises(ValueError):
            validate_username("")

    def test_message_validation(self):
        self.assertEqual(
            validate_message(" hello "),
            "hello",
        )

        with self.assertRaises(ValueError):
            validate_message("")


if __name__ == "__main__":
    unittest.main()
