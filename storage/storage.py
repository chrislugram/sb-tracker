"""
This file contains a storage module that saves data into local
storage with .parquet
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import pandas as pd

from config.app_config import AppConfig
from logger import get_logger

log = get_logger("storage")


class StorageCollection(Enum):
    timetrack = "TIMETRACK"
    projects = "PROJECTS"
    expenses = "EXPENSES"
    infoices = "INVOICES"


@dataclass
class Storage:
    """
    This class is a storage module that saves data into local
    storage with .parquet
    """

    config: AppConfig = None
    _cache_data: dict = field(default_factory=dict)

    def load_all(self):
        """
        Load all the data from the storage system

        Returns:
            dict: Dictionary of dataframes
        """
        for col in StorageCollection:
            self.load(col)

    def load(self, col: StorageCollection) -> pd.DataFrame:
        """
        Load the data from the storage system

        Args:
            col (StorageCollection): Storage collection

        Returns:
            pd.DataFrame: Generic dataframe
        """
        log.info(col.name)
        file_col = Path(self.config.get(col.value, "path"))

        if file_col.exists():
            log.info(f"Loading {file_col}")
        else:
            log.info("File does not exist")

    def save(self, data: pd.DataFrame):
        """
        Save the data to the storage system

        Args:
            data (pd.DataFrame): Generic dataframe
        """
        pass
