import copy
import os
import json
import pickle
from kadai.utils import FileUtils

class ConfigHandler():
    def __init__(self):
        self.config_file_path = os.path.join(FileUtils.getConfigPath(), 'config.json')
        self.config_file_out_path = self.config_file_path
        self.config_default = {
            'engine': 'vibrance',
            'data_directory': FileUtils.getDataPath(),
            'cache_directory': FileUtils.getCachePath(),
            'light': False,
            'progress': False,
            'debug': False
        }

        self.config = parse_config(self.config_default, self.config_file_path)

    def setConfigFilePath(self, path):
        self.config_file_path = path
        self.config = parse_config(self.config_default, self.config_file_path)

    def setConfigFileOutPath(self, path):
        self.config_file_out_path = path

    def get(self):
        return self.config

    def save(self):
        config_path = os.path.dirname(self.config_file_out_path)
        if not os.path.isdir(config_path):
            os.mkdir(config_path)

        with open(self.config_file_out_path, 'wb') as config_file:
            config_file.write(json.dumps(self.config,
                indent=4, separators=(',',': ')).encode('utf-8'))

    def load(self, config_file_path):
        with open(config_file_path, 'rb') as config_file:
            self.config = json.load(config_file)

def compareFlagWithConfig(flag, config_option):
    if(flag):
        return flag
    else:
        return config_option

def parse_config(config_default, config_file_path):
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