"""
This class contains the dataclass for definition
"""

import datetime
from dataclasses import dataclass, fields
from typing import List


@dataclass
class Definition:
    created_at: datetime.datetime

    @classmethod
    def get_column_names(cls) -> List[str]:
        """
        Get the column names

        Returns:
            List[str]: List of column names
        """
        return [f.name for f in fields(cls)]
