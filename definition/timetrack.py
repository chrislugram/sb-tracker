"""
This file contains the dataclass for definition of timetrack
"""

import datetime
from dataclasses import dataclass, field


@dataclass
class Timetrack:
    project: str
    duration: int
    name: str
    description: str
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.project} - {self.created_at} - {self.duration} - {self.name} - {self.description}"
