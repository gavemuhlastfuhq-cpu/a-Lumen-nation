"""
Crisis-safety policy.

Lumen must distinguish:
- ordinary conversation,
- emotional distress,
- possible self-harm risk,
- imminent danger.

The system must never claim that an AI is a human responder.

This module deliberately does not attempt to diagnose a user.
It provides policy-level classification helpers for later
integration with a tested crisis-response workflow.
"""

from enum import Enum


class CrisisLevel(str, Enum):
    NONE = "none"
    DISTRESS = "distress"
    POSSIBLE_RISK = "possible_risk"
    IMMINENT_DANGER = "imminent_danger"


def response_requirements(level: CrisisLevel) -> dict:
    if level == CrisisLevel.NONE:
        return {
            "human_contact_recommended": False,
            "emergency_guidance": False,
        }

    if level == CrisisLevel.DISTRESS:
        return {
            "human_contact_recommended": True,
            "emergency_guidance": False,
        }

    if level == CrisisLevel.POSSIBLE_RISK:
        return {
            "human_contact_recommended": True,
            "emergency_guidance": True,
        }

    return {
        "human_contact_recommended": True,
        "emergency_guidance": True,
    }
