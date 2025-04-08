"""
This file contains a storage module that saves data into local storage with .parquet
"""

from dataclasses import dataclass, field, fields
from enum import Enum
from pathlib import Path

import pandas as pd

from config.app_config import AppConfig
from definition.expenses import Expense
from definition.invoice import Invoice
from definition.project import Project
from definition.timetrack import Timetrack
from logger import get_logger

log = get_logger("storage")


class StorageCollection(Enum):
    timetrack = "TIMETRACK"
    projects = "PROJECTS"
    expenses = "EXPENSES"
    invoices = "INVOICES"


@dataclass
class Storage:
    """
    This class is a storage module that saves data into local storage with .parquet
    """

    config: AppConfig = None
    _cache_data: dict = field(default_factory=dict)
    _base_path: Path = field(default_factory=Path)

    def __post_init__(self):

        if self.config is None:
            raise ValueError("config is required")

        self._base_path = Path(self.config.get("APPCONFIG", "base_path_storage"))
        if not self._base_path.exists():
            self._base_path.mkdir()

    def load_all(self):
        """
        Load all the data from the storage system

        Returns:
            dict: Dictionary of dataframes
        """
        for col in StorageCollection:
            self.load(col)

    def save_all(self):
        """
        Save all the data to the storage system
        """
        for col in StorageCollection:
            self.save(col)

    def load(self, col: StorageCollection) -> pd.DataFrame:
        """
        Load the data from the storage system

        Args:
            col (StorageCollection): Storage collection

        Returns:
            pd.DataFrame: Generic dataframe
        """
        # Get file name for collection
        file_col = self._base_path / self.config.get(col.value, "path")

        # Check if file exists
        if file_col.exists():
            log.info(f"Loading {file_col}")
            self._cache_data[col.value] = pd.read_parquet(file_col)
        else:
            log.info(f"File does not exist, creating {col.value}")
            dataclass_type = self._get_dataclass_type(col)
            column_names = [f.name for f in fields(dataclass_type)]
            self._cache_data[col.value] = pd.DataFrame(columns=column_names)

    def save(self, col: StorageCollection):
        """
        Save the data to the storage system
        """
        log.info(self._cache_data.keys())
        if col.value in self._cache_data.keys():
            file_col = self._base_path / self.config.get(col.value, "path")
            log.info(f"Saving {file_col}")
            self._cache_data[col.value].to_parquet(file_col)

    def get(self, col: StorageCollection) -> pd.DataFrame:
        """
        Get the data from the storage system

        Args:
            col (StorageCollection): Storage collection

        Returns:
            pd.DataFrame: Generic dataframe
        """
        return self._cache_data[col.value]

    def _get_dataclass_type(self, col: StorageCollection) -> type:
        """
        Get the dataclass type from the storage collection

        Args:
            col (StorageCollection): Storage collection

        Returns:
            type: Dataclass type
        """
        if col == StorageCollection.projects:
            return Project
        elif col == StorageCollection.timetrack:
            return Timetrack
        elif col == StorageCollection.expenses:
            return Expense
        elif col == StorageCollection.invoices:
            return Invoice
