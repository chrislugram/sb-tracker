"""
This file contains the dataclass for definition of timetrack
"""

from dataclasses import dataclass

from definition.definition import Definition


@dataclass
class Timetrack(Definition):
    project: str
    duration: int
    name: str
    description: str

    def __str__(self):
        return f"{self.project} - {self.created_at} - {self.duration} - {self.name} - {self.description}"
