import os.path

if "XDG_DATA_HOME" in os.environ:
	DATA_PATH = os.path.join(os.getenv("XDG_DATA_HOME"), 'kadai')
else:
	DATA_PATH = os.path.expanduser('~/.local/share/kadai')

if "XDG_CONFIG_HOME" in os.environ:
	CONFIG_PATH = os.path.join(os.getenv("XDG_CONFIG_HOME"), 'kadai')
else:
	CONFIG_PATH = os.path.expanduser('~/.config/kadai')

if "XDG_CACHE_HOME" in os.environ:
	CACHE_PATH = os.path.join(os.getenv("XDG_CACHE_HOME"), 'kadai')
else:
	CACHE_PATH = os.path.expanduser('~/.cache/kadai')

DEBUG_MODE = False

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