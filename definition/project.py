"""
This file contains the dataclass for definition of projects
"""

from dataclasses import dataclass

from definition.definition import Definition


@dataclass
class Project(Definition):
    name: str
    description: str
    id: str

    def __str__(self):
        return f"{self.id} - {self.name} - {self.created_at} - {self.description}"
