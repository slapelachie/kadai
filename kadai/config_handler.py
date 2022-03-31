"""
Config handler

kadai - Simple wallpaper manager for tiling window managers.
Copyright (C) 2020  slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Find the full license in the root of this project
"""

import copy
import os
import json

from kadai.utils import file_utils

DEFAULT_CONFIG = {
    "engine": "vibrance",
    "data_directory": file_utils.get_data_path(),
    "cache_directory": file_utils.get_cache_path(),
    "custom_theme_path": os.path.join(
        file_utils.get_config_path(), "themes/config.json"
    ),
    "light": False,
    "progress": False,
    "debug": False,
    "use_custom_theme": False,
}


class ConfigHandler:
    """The main config handler class"""

    def __init__(self):
        """The initialisation for the config class"""
        self._config_file_path = os.path.join(
            file_utils.get_config_path(), "config.json"
        )
        self._config_file_out_path = self._config_file_path
        self._config = parse_config(self._config_file_path)

    def set_config_file_path(self, path: str):
        """
        Sets the path for the config file and reloads it from the new path

        Arguments:
            path(str): the path to the config file
        """
        self._config_file_path = path
        self._config = parse_config(self._config_file_path)

    def get_config_file_path(self) -> str:
        """
        Gets the path for the config file

        Returns:
            (str): the path to the config file
        """
        return self._config_file_path

    def set_config_file_out_path(self, path: str):
        """
        Sets the the path where the config file will be exported to

        Arguments:
            path (str): the file path to export the config to
        """
        self._config_file_out_path = path

    def get_config_file_out_path(self) -> str:
        """
        Gets the export path for the config file

        Returns:
            (str): the export path to the config file
        """
        return self._config_file_out_path

    def set_config(self, config: dict):
        """
        Updates the current config with the parsed config

        Arguments:
            config (dict): what the replace the current config with
        """
        self._config = config

    def get_config(self) -> dict:
        """
        Gets the current config

        Returns:
            (dict): the current config
        """
        return self._config

    def save_config(self):
        """Saves the current config to the config_file_out_path"""
        config_path = os.path.dirname(self._config_file_out_path)
        if not os.path.isdir(config_path):
            os.mkdir(config_path)

        with open(self._config_file_out_path, "wb") as config_file:
            config_file.write(
                json.dumps(self._config, indent=4, separators=(",", ": ")).encode(
                    "utf-8"
                )
            )

    def load_config(self, config_file_path: str):
        """
        Loads and overrides the config from a given path

        Arguments:
            config_file_path (str): the path to the config file
        """
        with open(config_file_path, "rb") as config_file:
            self._config = json.load(config_file)


def parse_config(config_file_path: str) -> dict:
    """
    Parses the config by returning the config at the path, if it doesnt exist
    it will return the default config

    Arguments:
        config_file_path (str): the path to the config file

    Returns:
        (dict): the config file
    """
    config = copy.copy(DEFAULT_CONFIG)

    try:
        with open(config_file_path, "rb") as config_file:
            loaded_config = json.load(config_file)
            config.update(loaded_config)
    except IOError:
        pass

    return config
