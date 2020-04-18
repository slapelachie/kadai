#!/usr/bin/env python3

# KADAI
# Author: slapelachie
# Wallpaper / theme manager

import argparse
import sys
import os.path
import logging
import shutil
import random

from .settings import DATA_PATH, CONFIG_PATH, CACHE_PATH
from . import utils, log, theme

logger = log.setup_logger(__name__, logging.INFO, log.defaultLoggingHandler())

def get_args():
	""" Get the args parsed from the command line and does arg handling stuff """

	arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")

	arg.add_argument('-v', action='store_true',
		help='Verbose Logging')

	arg.add_argument('-q', action='store_true',
		help='Allow only error logging')
		
	arg.add_argument("-g", action="store_true",
		help="generate themes")
	
	arg.add_argument("-i", metavar="\"path/to/dir\"",
		help="the input file")
	
	arg.add_argument("-p", action="store_true",
		help="Use last set theme")

	arg.add_argument('--override', action="store_true",
		help="Override exisiting themes")
	
	arg.add_argument("--clear", action="store_true",
		help="Clear all data relating to KADAI")

	return arg

def parse_args(parser):
	"""
	Parses the arguments onto different actions

	Arguments:
		parser (idk) -- the argument parser
	"""

	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	VERBOSE_MODE = True if args.v else False

	if args.q:
		pass

	if args.i:
		if args.g:
			theme.generate(args.i, os.path.join(DATA_PATH, 'templates/'), CACHE_PATH, args.override)
			sys.exit(0)
		else:
			images = utils.get_image_list(args.i)
			random.shuffle(images)
			image = utils.get_image(images[0])

			# If the theme file does not exist generate it and then update to it
			try:
				theme.update(image, CACHE_PATH, post_scripts=True)
			except theme.noPreGenThemeError:
				theme.generate(image, os.path.join(DATA_PATH, 'templates/'),
					CACHE_PATH, args.override)
				theme.update(image, CACHE_PATH, post_scripts=True)
			sys.exit(0)
	elif args.p:
		# Check if the cached image exists, if it does update to that
		last_image = os.path.join(CACHE_PATH, "image")
		if(utils.check_if_image(last_image)):
			theme.update(last_image, CACHE_PATH, post_scripts=True)
		else:
			logger.critical("Last image invalid or does not exist!")
			sys.exit(1)
	
	elif args.clear:
		clear = input("Are you sure you want to remove the cache relating to KADAI? [y/N] ").lower()
		if(clear == "y"):
			try:
				shutil.rmtree(CACHE_PATH)
			except:
				raise
			logger.info("Cleared KADAI cache folders")
		else:
			logger.warning("Canceled clearing cache folders...")
	else:
		logger.critical("No file specified...")
		sys.exit(1)

def main():
	# Create required directories
	try:
		os.makedirs(CACHE_PATH, exist_ok=True)
		os.makedirs(DATA_PATH, exist_ok=True)
		os.makedirs(CONFIG_PATH, exist_ok=True)
	except:
		raise

	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()