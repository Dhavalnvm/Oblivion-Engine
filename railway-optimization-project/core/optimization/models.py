# core/optimization/models.py
"""
Data models for optimization problems.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Train:
    """Train data model."""
    train_id: str
    arrival_time: datetime
    departure_time: datetime
    platform: Optional[str] = None
    delay_minutes: int = 0
    capacity: int = 200
    train_type: str = "EXPRESS"


@dataclass
class Platform:
    """Platform data model."""
    platform_id: str
    capacity: int = 1
    is_available: bool = True
    maintenance_window: Optional[tuple] = None


@dataclass
class OptimizationProblem:
    """Complete optimization problem definition."""
    trains: List[Train]
    platforms: List[Platform]
    time_window_start: datetime
    time_window_end: datetime
    objectives: List[str] = None

    def __post_init__(self):
        if self.objectives is None:
            self.objectives = ["minimize_delays", "maximize_utilization"]


