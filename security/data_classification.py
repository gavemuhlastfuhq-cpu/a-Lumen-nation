"""
Lumen data classification.

Classification is intentionally explicit. A component must not
silently treat sensitive information as ordinary application data.
"""

from enum import Enum


class DataClass(str, Enum):
    PUBLIC = "public"
    USER_CONTENT = "user_content"
    PRIVATE = "private"
    SENSITIVE = "sensitive"
    CRISIS = "crisis"
    SECURITY = "security"


class Retention(str, Enum):
    MINIMUM_REQUIRED = "minimum_required"
    USER_CONTROLLED = "user_controlled"
    LEGAL_HOLD = "legal_hold"


def requires_explicit_purpose(data_class: DataClass) -> bool:
    return data_class in {
        DataClass.PRIVATE,
        DataClass.SENSITIVE,
        DataClass.CRISIS,
        DataClass.SECURITY,
    }
