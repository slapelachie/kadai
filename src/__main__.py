#!/usr/bin/env python3

# KADAI
# Author: Slapaay
# Wallpaper and lockscreen theme manager

#TODO: Create a makescript
#TODO: Allow the user to clear or override themes / lockscreens
#TODO: Template files need to go somewhere

import argparse
import sys
import os.path
import logging

from utils.settings import DATA_DESKTOP_PATH, DATA_LOCKSCREEN_PATH, DATA_PATH, CONFIG_PATH
from utils import utils,log
from generators.theme import ThemeGenerator
from generators.lockscreen import LockscreenGenerate

logger = log.setup_logger(__name__, logging.INFO, log.defaultLoggingHandler())

def get_args():
	""" Get the args parsed from the command line and does arg handling stuff """

	arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")
	subparser = arg.add_subparsers(help='sub-command help', dest="subcommand")

	arg.add_argument('-v', action='store_true',
		help='Verbose Logging')

	arg.add_argument('-q', action='store_true',
		help='Allow only error logging')
		
	wall_arg = subparser.add_parser('wallpaper', help="Wallpaper related commands") 
	lock_arg = subparser.add_parser('lockscreen', help="Lockscreen related commands") 	

	wall_arg.add_argument("-g", action="store_true",
			help="generate themes")
	
	wall_arg.add_argument("-i", metavar="\"path/to/dir\"",
			help="the input file")

	wall_arg.add_argument("-l", action="store_true",
			help="generate and apply lockscreen")
	
	wall_arg.add_argument("-p", action="store_true",
		help="Use last set theme")
	
	lock_arg.add_argument("-g", action="store_true",
			help="generate themes")

	lock_arg.add_argument("-i", metavar="\"path/to/dir\"",
		help="The input file or directory")


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

	# If the subcommand 'wallpaper' is called
	if args.subcommand == "wallpaper":
		if args.i:
			if args.g:
				ThemeGenerator(args.i, VERBOSE_MODE).generate()
				sys.exit(0)
			else:
				ThemeGenerator(args.i, VERBOSE_MODE).update(args.l)
				sys.exit(0)
		elif args.p:
			# Check if the last file exists, if it does update to that
			if(os.path.isfile(os.path.join(DATA_DESKTOP_PATH, "last"))):
				with open(os.path.join(DATA_DESKTOP_PATH, "last"), "r") as file:
					filedata = str(file.read()).rstrip()
					ThemeGenerator(filedata, VERBOSE_MODE).update(args.l)
			else:
				logger.critical("Last file does not exist!")
				sys.exit(1)
		else:
			logger.critical("No file specified...")
			sys.exit(1)
	# If the subcommand 'lockscreen' is called
	elif args.subcommand == "lockscreen":
		if args.i:
			if args.g:
				LockscreenGenerate(args.i, VERBOSE_MODE).generate()
			else:
				LockscreenGenerate(args.i, VERBOSE_MODE).update()	

def main():
	# Create required directories
	os.makedirs(DATA_PATH, exist_ok=True)
	os.makedirs(DATA_DESKTOP_PATH, exist_ok=True)
	os.makedirs(DATA_LOCKSCREEN_PATH, exist_ok=True)
	os.makedirs(CONFIG_PATH, exist_ok=True)

	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()