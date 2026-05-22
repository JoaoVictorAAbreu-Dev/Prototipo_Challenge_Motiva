"""
Repository Interfaces - Abstract definitions for data persistence
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.microsegment import MicroSegment
from app.domain.entities.monitor import Monitor


class MonitorRepository(ABC):
    """Abstract repository for Monitor entity"""

    @abstractmethod
    async def save(self, monitor: Monitor) -> Monitor:
        """Save a monitor"""
        pass

    @abstractmethod
    async def get_by_id(self, monitor_id: str) -> Optional[Monitor]:
        """Get monitor by ID"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Monitor]:
        """Get all monitors with pagination"""
        pass

    @abstractmethod
    async def find_by_status(
        self, status: str, skip: int = 0, limit: int = 20
    ) -> List[Monitor]:
        """Find monitors by status"""
        pass

    @abstractmethod
    async def delete(self, monitor_id: str) -> bool:
        """Delete a monitor"""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total monitors"""
        pass


class MicroSegmentRepository(ABC):
    """Abstract repository for operational microsegments."""

    @abstractmethod
    async def save_many(self, microsegments: list[MicroSegment]) -> None:
        """Save many microsegments in a single batch."""
        pass

    @abstractmethod
    async def get_by_id(self, microsegment_id: str) -> Optional[MicroSegment]:
        """Get microsegment by ID."""
        pass

    @abstractmethod
    async def get_all(
        self, skip: int = 0, limit: int = 250
    ) -> List[MicroSegment]:
        """List microsegments with pagination."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total microsegments."""
        pass
