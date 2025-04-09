import shutil
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from config.app_config import AppConfig
from definition.project import Project
from storage.storage import Storage, StorageCollection


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.config = AppConfig("config_test.ini")
        self.config.config["APPCONFIG"]["base_path_storage"] = (
            Path.cwd() / "test_storage"
        ).as_posix()
        self.storage = Storage(config=self.config)

    def tearDown(self):
        shutil.rmtree(Path.cwd() / "test_storage")

    def test_init(self):
        self.assertIsNotNone(self.storage.config)
        self.assertIsInstance(self.storage._cache_data, dict)
        self.assertIsInstance(self.storage._base_path, Path)

    def test_post_init(self):
        self.storage.config = None
        with self.assertRaises(ValueError):
            self.storage.__post_init__()

        self.storage.config = self.config
        self.storage.__post_init__()
        self.assertIsNotNone(self.storage._base_path)

    @patch("pathlib.Path.exists", return_value=False)
    @patch("pathlib.Path.mkdir")
    def test_post_init_create_base_path(self, mock_mkdir, mock_exists):
        self.storage.__post_init__()
        mock_exists.assert_called_once()
        mock_mkdir.assert_called_once()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.mkdir")
    def test_post_init_do_not_create_base_path(self, mock_mkdir, mock_exists):
        self.storage.__post_init__()
        mock_exists.assert_called_once()
        mock_mkdir.assert_not_called()

    def test_load(self):
        for col in StorageCollection:
            self.storage._cache_data = {}

            self.storage.load(col)
            self.assertIsNotNone(self.storage._cache_data[col.value])
            self.assertIsInstance(self.storage._cache_data[col.value], pd.DataFrame)

    def test_save(self):
        for col in StorageCollection:
            self.storage._cache_data[col.value] = pd.DataFrame({"a": [1, 2, 3]})

            self.storage.save(col)
            self.assertIsNotNone(self.storage._cache_data[col.value])
            self.assertIsInstance(self.storage._cache_data[col.value], pd.DataFrame)

    def test_load_all(self):
        self.storage.load = MagicMock()
        self.storage.load_all()
        self.storage.load.call_count = 4

    def test_save_all(self):
        self.storage.save = MagicMock()
        self.storage.save_all()
        self.storage.save.call_count = 4

    def test_add_to_collection(self):
        # Given an empty collection
        self.storage._cache_data = {}
        self.storage.load(StorageCollection.projects)

        # When adding an item to the collection
        project = Project(
            id="1",
            name="Project 1",
            description="Description 1",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.storage.add_to_collection(StorageCollection.projects, project)

        # Then
        self.assertIn("PROJECTS", self.storage._cache_data.keys())
        self.assertEqual(len(self.storage._cache_data["PROJECTS"]), 1)
        self.assertIsInstance(self.storage._cache_data["PROJECTS"], pd.DataFrame)
        self.assertEqual(
            self.storage._cache_data["PROJECTS"].iloc[0]["name"], "Project 1"
        )
