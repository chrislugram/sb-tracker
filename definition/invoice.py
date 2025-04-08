"""
This file contains the dataclass for definition of invoice
"""

import datetime
from dataclasses import dataclass, field


@dataclass
class Invoice:
    project: str
    platform: str
    sales: int
    price: float
    commission: float
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.project} - {self.created_at} - {self.platform} - {self.sales} - {self.price} - {self.commission}"
