import logging
import tqdm
import sys

default_format = ("[%(levelname)s\033[0m] "
	"\033[1;31m%(module)s\033[0m: "
	"%(message)s")

bar_format='{percentage:3.0f}% {n}/{total}'

class TqdmLoggingHandler(logging.Handler):
	def __init__(self, level=logging.NOTSET):
		super().__init__(level)

	"""def emit(self, record):
		try:
			self.setFormatter(logging.Formatter(default_format))
			msg = self.format(record)
			tqdm.tqdm.write(msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)"""

class defaultLoggingHandler(logging.StreamHandler):
	"""def emit(self, record):
		try:
			self.setFormatter(logging.Formatter(default_format+'\n'))
			msg = self.format(record)
			stream = self.stream
			stream.write(msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)	"""

def setup_logger(name, handler, level=logging.WARNING):
	""" Sets up the logger """	
	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)
	return logger

logging.addLevelName(logging.ERROR, '\033[1;31mE')
logging.addLevelName(logging.INFO, '\033[1;32mI')
logging.addLevelName(logging.WARNING, '\033[1;33mW')
logging.addLevelName(logging.CRITICAL, '\033[1;33mC')
logging.addLevelName(logging.DEBUG, '\033[1;33mD')

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