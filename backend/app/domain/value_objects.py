"""
Domain Value Objects
Immutable, self-validating value objects
"""

from dataclasses import dataclass
from enum import Enum


class StatusEnum(str, Enum):
    """Status enumeration"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class Coordinate:
    """Represents a geographic coordinate (lat/lon)"""

    latitude: float
    longitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    def to_dict(self) -> dict:
        return {"latitude": self.latitude, "longitude": self.longitude}


@dataclass(frozen=True)
class BoundingBox:
    """Represents a geographic bounding box"""

    min_latitude: float
    min_longitude: float
    max_latitude: float
    max_longitude: float

    def __post_init__(self):
        if self.min_latitude > self.max_latitude:
            raise ValueError("min_latitude must be less than max_latitude")
        if self.min_longitude > self.max_longitude:
            raise ValueError("min_longitude must be less than max_longitude")

    def to_dict(self) -> dict:
        return {
            "min_latitude": self.min_latitude,
            "min_longitude": self.min_longitude,
            "max_latitude": self.max_latitude,
            "max_longitude": self.max_longitude,
        }


@dataclass(frozen=True)
class EntityId:
    """Value object for entity identifiers"""

    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("EntityId value cannot be empty")

    def __str__(self) -> str:
        return self.value


class CriticityLevel(str, Enum):
    """Operational criticity levels"""

    LOW = "baixo"
    MODERATE = "moderado"
    HIGH = "alto"
    CRITICAL = "crítico"


@dataclass(frozen=True)
class Percentage:
    """Percentage-like value object constrained to 0-100"""

    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 100:
            raise ValueError("Percentage value must be between 0 and 100")

    def normalized(self) -> float:
        return self.value / 100


@dataclass(frozen=True)
class DaysWithoutMaintenance:
    """Non-negative number of days without maintenance"""

    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Days without maintenance cannot be negative")

    def normalized(self, saturation_days: int = 90) -> float:
        if saturation_days <= 0:
            raise ValueError("saturation_days must be greater than zero")
        return min(self.value / saturation_days, 1.0)


@dataclass(frozen=True)
class ContractualWeight:
    """Contractual weight constrained to 1-5"""

    value: int

    def __post_init__(self):
        if not 1 <= self.value <= 5:
            raise ValueError("Contractual weight must be between 1 and 5")

    def normalized(self) -> float:
        return self.value / 5
