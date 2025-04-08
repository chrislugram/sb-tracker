"""
This class is the configuration for the app using yaml
"""

from configparser import ConfigParser


class AppConfig:
    """
    This class is the configuration for the app
    """
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get(self, section: str, key: str) -> str:
        """
        Get a value from the config file

        Args:
            section (str): The section of the config file
            key (str): The key of the config file

        Returns:
            str: The value of the config file
        """
        return self.config.get(section, key)


