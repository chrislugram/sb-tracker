"""
This file contains the dataclass for definition of expenses
"""

from dataclasses import dataclass

from definition.definition import Definition


@dataclass
class Expense(Definition):
    project: str
    type: str
    detail: str
    amount: float

    def __str__(self):
        return f"{self.project} - {self.created_at} - {self.type} - {self.detail} - {self.amount}"
