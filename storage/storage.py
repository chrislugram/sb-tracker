"""
This file contains a storage module that saves data into local storage with .parquet
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd

@dataclass
class Storage():
    """
    This class is a storage module that saves data into local storage with .parquet
    """
    # data: pd.DataFrame = field(default_factory=pd.DataFrame)
    # path: Optional[str] = None
    
    def load(self) -> pd.DataFrame:
        """
        Load the data from the storage system

        Returns:
            pd.DataFrame: Generic dataframe
        """
        pass
    
    def save(self, data: pd.DataFrame):
        """
        Save the data to the storage system

        Args:
            data (pd.DataFrame): Generic dataframe
        """
        pass