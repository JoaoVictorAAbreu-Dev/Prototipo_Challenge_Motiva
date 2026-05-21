"""
Logistics compliance buffer entity
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LogisticsComplianceDecision:
    """Decision for strategically holding an order"""

    hold_order: bool
    hold_hours: int
    logistic_compensation_score: float
    status_label: str
    operational_justification: str
