import copy
import os
import json
import pickle
from kadai.utils import file_utils


class ConfigHandler:
    def __init__(self):
        self.config_file_path = os.path.join(
            file_utils.get_config_path(), "config.json"
        )
        self.config_file_out_path = self.config_file_path
        self.config_default = {
            "engine": "vibrance",
            "data_directory": file_utils.get_data_path(),
            "cache_directory": file_utils.get_cache_path(),
            "light": False,
            "progress": False,
            "debug": False,
        }

        self.config = parse_config(self.config_default, self.config_file_path)

    def set_config_path(self, path: str) -> None:
        self.config_file_path = path
        self.config = parse_config(self.config_default, self.config_file_path)

    def set_config_file_out_path(self, path: str) -> None:
        self.config_file_out_path = path

    def get(self) -> dict:
        return self.config

    def save(self) -> None:
        config_path = os.path.dirname(self.config_file_out_path)
        if not os.path.isdir(config_path):
            os.mkdir(config_path)

        with open(self.config_file_out_path, "wb") as config_file:
            config_file.write(
                json.dumps(self.config, indent=4, separators=(",", ": ")).encode(
                    "utf-8"
                )
            )

    def update(self, config: dict) -> None:
        self.config = config

    def load(self, config_file_path: str) -> None:
        with open(config_file_path, "rb") as config_file:
            self.config = json.load(config_file)


def compare_flag_with_config(flag, config_option):
    if flag:
        return flag
    else:
        return config_option


def parse_config(config_default: dict, config_file_path: str) -> dict:
    config = copy.copy(config_default)

    try:
        with open(config_file_path) as config_file:
            loaded_config = json.load(config_file)
            config.update(loaded_config)
    except IOError:
        pass

    return config


"""
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