import logging
import tqdm
import sys

default_format = ("[%(levelname)s\033[0m] "
	"\033[1;31m%(module)s\033[0m: "
	"%(message)s")

class TqdmLoggingHandler(logging.Handler):
	def __init__(self, level=logging.NOTSET):
		super().__init__(level)

	def emit(self, record):
		try:
			self.setFormatter(logging.Formatter(default_format))
			msg = self.format(record)
			tqdm.tqdm.write(msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

class defaultLoggingHandler(logging.StreamHandler):
	def emit(self, record):
		try:
			self.setFormatter(logging.Formatter(default_format+'\n'))
			msg = self.format(record)
			stream = self.stream
			stream.write(msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)	

def setup_logger(name, level, handler):
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