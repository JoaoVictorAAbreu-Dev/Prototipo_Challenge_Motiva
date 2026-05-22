from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationScenario:
    name: str
    horizon_weeks: int
    description: str
