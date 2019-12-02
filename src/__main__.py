#!/usr/bin/env python3

# KADAI
# Author: Slapaay
# Wallpaper and lockscreen theme manager

import argparse
import sys
import os.path
import imghdr
import random
import importlib
import hashlib
import subprocess
import glob

from utils.settings import CACHE_DESKTOP_PATH, CACHE_LOCKSCREEN_PATH, CACHE_PATH, CONFIG_PATH
from generators.theme import ThemeGenerator
from generators.lockscreen import LockscreenGenerate

def error_msg(msg):
	print("[ERROR]: " + msg)

def get_args():
	arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")
	subparser = arg.add_subparsers(help='sub-command help', dest="subcommand")
	
	wall_arg = subparser.add_parser('wallpaper', help="Wallpaper related commands") 
	lock_arg = subparser.add_parser('lockscreen', help="Lockscreen related commands") 

	wall_arg.add_argument("-p", "--previous", action="store_true",
		help="Use last set theme")

	wall_arg.add_argument("-i", metavar="\"path/to/dir\"",
			help="the input file")

	wall_arg.add_argument("-g", action="store_true",
			help="generate themes")

	wall_arg.add_argument("-r", action="store_true",
			help="regenerate the theme")

	wall_arg.add_argument("-l", action="store_true",
			help="generate and apply lockscreen")

	lock_arg.add_argument("-i", metavar="\"path/to/dir\"",
		help="The input file or directory")

	lock_arg.add_argument("-g", action="store_true",
			help="generate themes")

	lock_arg.add_argument("-r", action="store_true",
			help="regenerate the theme")

	return arg

def parse_args(parser):
	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	if args.subcommand == "wallpaper":
		if args.i:
			if args.g:
				ThemeGenerator(args.i).generate()
				sys.exit(0)
			else:
				ThemeGenerator(args.i).update(args.l)
				sys.exit(0)
		elif args.p:
			if(os.path.isfile(os.path.join(CACHE_DESKTOP_PATH, "last"))):
				with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "r") as file:
					filedata = str(file.read()).rstrip()
					ThemeGenerator(filedata).update(args.l)
			else:
				error_msg("Last file does not exist!")
				sys.exit(1)
		else:
			error_msg("No file specified...")
			sys.exit(1)

	elif args.subcommand == "lockscreen":
		if args.i:
			if args.g:
				LockscreenGenerate(args.i).generate()
			else:
				LockscreenGenerate(args.i).update()	

def main():
	os.makedirs(CACHE_PATH, exist_ok=True)
	os.makedirs(CACHE_DESKTOP_PATH, exist_ok=True)
	os.makedirs(CACHE_LOCKSCREEN_PATH, exist_ok=True)
	os.makedirs(CONFIG_PATH, exist_ok=True)
	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()