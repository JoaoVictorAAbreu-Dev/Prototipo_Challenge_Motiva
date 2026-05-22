from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationProjectionSummary:
    total_microsegments: int
    critical_count: int
    average_ipo: float
    average_future_priority_48h: float


@dataclass(frozen=True)
class SimulationProjectionResponse:
    horizon_weeks: float
    items: list[dict]
    summary: SimulationProjectionSummary
