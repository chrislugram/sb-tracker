"""
This file contains the main function for the app
"""

from config.app_config import AppConfig
from logger import get_logger
from storage.storage import Storage

# Create and configure logger
log = get_logger("main")

# Load app configuration
app_config = AppConfig("config.ini")

# Load storage
storage = Storage(config=app_config)
storage.load_all()

# Save storage
storage.save_all()
