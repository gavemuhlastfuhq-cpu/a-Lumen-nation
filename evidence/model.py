"""
Epistemic model for Lumen.

The purpose is to keep claims, observations, evidence, sources,
interpretations, and conclusions from being collapsed into one
undifferentiated "answer".
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EvidenceStatus(str, Enum):
    UNASSESSED = "UNASSESSED"
    SUPPORTED = "SUPPORTED"
    STRONGLY_SUPPORTED = "STRONGLY_SUPPORTED"
    CONTESTED = "CONTESTED"
    UNRESOLVED = "UNRESOLVED"
    CONTRADICTED = "CONTRADICTED"
    DISPROVEN = "DISPROVEN"


class EpistemicType(str, Enum):
    OBSERVATION = "OBSERVATION"
    CLAIM = "CLAIM"
    EVIDENCE = "EVIDENCE"
    SOURCE = "SOURCE"
    INTERPRETATION = "INTERPRETATION"
    CONTRADICTION = "CONTRADICTION"
    CONCLUSION = "CONCLUSION"
    DECISION = "DECISION"


@dataclass
class EvidenceItem:
    id: str
    kind: EpistemicType
    content: str
    status: EvidenceStatus = EvidenceStatus.UNASSESSED
    source_id: Optional[str] = None
    parent_ids: list[str] = field(default_factory=list)
    confidence: Optional[float] = None

    def validate(self):
        if not self.id.strip():
            raise ValueError("Evidence ID is required.")

        if not self.content.strip():
            raise ValueError("Evidence content is required.")

        if self.confidence is not None:
            if not 0.0 <= self.confidence <= 1.0:
                raise ValueError(
                    "Confidence must be between 0 and 1."
                )
