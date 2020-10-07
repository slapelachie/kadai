import copy
import os
import json
import pickle
from kadai import settings

config_file_path = os.path.join(settings.CONFIG_PATH, 'config.json')

config_default = {
    'engine': 'vibrance',
    'out_directory': '$HOME/.local/share/',
    'light_theme': False,
    'progress': False,
    'debug': False
}

def parse_config():
    config = copy.copy(config_default)
    
    try:
        with open(config_file_path) as config_file:
            loaded_config = json.load(config_file)
            config.update(loaded_config)
    except IOError:
        save_config(config)
    
    return config

def save_config(config_dict):
    config_path = os.path.dirname(config_file_path)
    if not os.path.isdir(config_path):
        os.mkdir(config_path)

    with open(config_file_path, 'wb') as config_file:
        config_file.write(json.dumps(config_dict,
            indent=4, separators=(',',': ')).encode('utf-8'))

def load_config(config_file_path):
    with open(config_file_path, 'rb') as config_file:
        return pickle.load(config_file, encoding='utf-8')

def compareFlagWithConfig(flag, config_option):
    if(flag):
        return flag
    else:
        return config_option

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