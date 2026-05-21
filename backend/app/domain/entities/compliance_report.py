"""
Compliance report entities
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceSnapshot:
    """Before/after evidence descriptor"""

    title: str
    summary: str


@dataclass(frozen=True)
class ComplianceReport:
    """Digital compliance dossier for ANTT evidence"""

    segment_id: str
    segment_name: str
    generated_at: str
    ipo: float
    criticity: str
    operational_evidence: str
    maintenance_history: str
    contractual_compliance: str
    before_snapshot: EvidenceSnapshot
    after_snapshot: EvidenceSnapshot
