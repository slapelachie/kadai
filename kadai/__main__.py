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

from kadai import log
from kadai.settings import DATA_PATH, CONFIG_PATH, CACHE_PATH
from kadai.utils import FileUtils
from kadai.themer import Themer

logger = log.setup_logger(__name__, logging.WARNING, log.defaultLoggingHandler())

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

	arg.add_argument("--backend", metavar="name",
		help="vibrance/hue")

	arg.add_argument("--progress", action="store_true",
		help="Show progress of theme generation")

	arg.add_argument("--warranty", action="store_true",
		help="Show the programs warranty")

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

	if args.warranty:
		print("""Copyright (C) 2020 slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.""")
		exit(0)

	if args.i:
		themer = Themer(args.i, DATA_PATH)
		themer.setEngine(args.backend)
		themer.setOverride(args.override)
		themer.disableProgress(False if args.progress else True)

		if args.g:
			themer.generate()
			sys.exit(0)
		else:
			# If the theme file does not exist generate it and then update to it
			try:
				themer.update()
			except FileUtils.noPreGenThemeError:
				themer.generate()
				themer.update()
			sys.exit(0)
	elif args.p:
		# Check if the cached image exists, if it does update to that
		last_image = os.path.join(DATA_PATH, "image")
		if(FileUtils.check_if_image(last_image)):
			themer = Themer(last_image, DATA_PATH)
			themer.update()
		else:
			logger.critical("Last image invalid or does not exist!")
			sys.exit(1)
	
	elif args.clear:
		clear = input("Are you sure you want to remove the cache relating to KADAI? [y/N] ").lower()
		if(clear == "y"):
			try:
				shutil.rmtree(DATA_PATH)
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