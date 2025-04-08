"""
This file contains the main function for the app
"""
import logging

from config.app_config import AppConfig

# Create and configure logger
logging.basicConfig(filename="sb.tracker.log", level=logging.INFO)
logger = logging.getLogger(__name__)

# Load app configuration
app_config = AppConfig("config.ini")

print(app_config.get("APPCONFIG", "cost_per_hour"))