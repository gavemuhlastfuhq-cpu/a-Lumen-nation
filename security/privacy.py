"""
Privacy guardrails.

These functions do not attempt to provide cryptographic security.
They provide application-level rules about what the application
should collect and expose.
"""

from .data_classification import DataClass


def can_collect(data_class: DataClass, purpose: str) -> bool:
    """
    Collection of non-public information requires a non-empty,
    explicitly defined purpose.
    """
    if data_class == DataClass.PUBLIC:
        return True

    return bool(
        isinstance(purpose, str)
        and purpose.strip()
    )


def should_disclose(
    data_class: DataClass,
    *,
    user_requested: bool = False,
    authorized_safety_process: bool = False,
) -> bool:
    """
    Default-deny disclosure for private/sensitive material.

    Emergency/safety disclosure is deliberately represented as a
    separate authorized process rather than an automatic AI decision.
    """
    if data_class == DataClass.PUBLIC:
        return True

    if user_requested:
        return True

    if authorized_safety_process:
        return True

    return False
