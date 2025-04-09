"""
This file contains the dataclass for definition of invoice
"""

from dataclasses import dataclass

from definition.definition import Definition


@dataclass
class Invoice(Definition):
    project: str
    platform: str
    sales: int
    price: float
    commission: float

    def __str__(self):
        return f"{self.project} - {self.created_at} - {self.platform} - {self.sales} - {self.price} - {self.commission}"
