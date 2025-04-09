"""
This class contains the dataclass for definition
"""

import datetime
from dataclasses import dataclass, field, fields
from typing import List


@dataclass
class Definition:
    created_at: datetime.datetime = field(init=False)

    def __post_init__(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_column_names(cls) -> List[str]:
        """
        Get the column names

        Returns:
            List[str]: List of column names
        """
        return [f.name for f in fields(cls)]
