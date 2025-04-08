"""
This file contains the dataclass for definition of projects
"""

import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.created_at} - {self.description}"
