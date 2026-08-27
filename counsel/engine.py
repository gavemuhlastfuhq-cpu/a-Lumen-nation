"""
Lumen counsel framework.

Counsel components provide independent analytical perspectives.
They do not directly authorize high-impact actions.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CounselRole:
    name: str
    purpose: str


COUNSEL_ROLES = (
    CounselRole(
        "Evidence",
        "Evaluate evidentiary support."
    ),
    CounselRole(
        "Provenance",
        "Trace where information originated and how it changed."
    ),
    CounselRole(
        "Logic",
        "Check reasoning and inference."
    ),
    CounselRole(
        "Statistics",
        "Evaluate quantitative claims and uncertainty."
    ),
    CounselRole(
        "Privacy",
        "Identify unnecessary collection or disclosure."
    ),
    CounselRole(
        "Safety",
        "Identify foreseeable harm and safety risks."
    ),
    CounselRole(
        "Ethics",
        "Evaluate ethical implications."
    ),
    CounselRole(
        "LegalContext",
        "Separate legal claims from factual and moral claims."
    ),
    CounselRole(
        "Context",
        "Identify missing information and ambiguity."
    ),
    CounselRole(
        "DevilsAdvocate",
        "Actively challenge assumptions and conclusions."
    ),
    CounselRole(
        "Synthesis",
        "Present the strongest supported synthesis while preserving disagreement."
    ),
)


def counsel_count() -> int:
    return len(COUNSEL_ROLES)


def is_odd_counsel_count() -> bool:
    return counsel_count() % 2 == 1


def validate_counsel():
    if not is_odd_counsel_count():
        raise RuntimeError(
            "Counsel count must remain odd."
        )

    names = [role.name for role in COUNSEL_ROLES]

    if len(names) != len(set(names)):
        raise RuntimeError(
            "Counsel roles must be unique."
        )


def record_disagreement(
    role: str,
    position: str,
    reason: str,
    resolving_evidence: str = "",
) -> dict:
    """
    Preserve disagreement instead of forcing artificial consensus.
    """
    return {
        "role": role,
        "position": position,
        "reason": reason,
        "resolving_evidence": resolving_evidence,
    }
