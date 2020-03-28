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