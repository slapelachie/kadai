#!/usr/bin/env python3

# KADAI
# Author: Slapaay
# Wallpaper and lockscreen theme manager

import argparse
import sys
import os.path
import logging

from utils.settings import CACHE_DESKTOP_PATH, CACHE_LOCKSCREEN_PATH, CACHE_PATH, CONFIG_PATH
from utils import utils
from generators.theme import ThemeGenerator
from generators.lockscreen import LockscreenGenerate

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

	if args.v:
		logging.getLogger().setLevel(15)

	if args.q:
		logging.getLogger().setLevel(logging.ERROR)
		sys.stdout = sys.stderr = open(os.devnull, "w")

	# If the subcommand 'wallpaper' is called
	if args.subcommand == "wallpaper":
		if args.i:
			if args.g:
				ThemeGenerator(args.i).generate()
				sys.exit(0)
			else:
				ThemeGenerator(args.i).update(args.l)
				sys.exit(0)
		elif args.p:
			# Check if the last file exists, if it does update to that
			if(os.path.isfile(os.path.join(CACHE_DESKTOP_PATH, "last"))):
				with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "r") as file:
					filedata = str(file.read()).rstrip()
					ThemeGenerator(filedata).update(args.l)
			else:
				logging.critical("Last file does not exist!")
				sys.exit(1)
		else:
			logging.critical("No file specified...")
			sys.exit(1)
	# If the subcommand 'lockscreen' is called
	elif args.subcommand == "lockscreen":
		if args.i:
			if args.g:
				LockscreenGenerate(args.i).generate()
			else:
				LockscreenGenerate(args.i).update()	

def main():
	# Create required directories
	os.makedirs(CACHE_PATH, exist_ok=True)
	os.makedirs(CACHE_DESKTOP_PATH, exist_ok=True)
	os.makedirs(CACHE_LOCKSCREEN_PATH, exist_ok=True)
	os.makedirs(CONFIG_PATH, exist_ok=True)

	utils.setup_logger()
	logging.getLogger().setLevel(logging.INFO)
	logging.getLogger().addHandler(utils.TqdmLoggingHandler())

	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()