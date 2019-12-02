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
from generators import wallpaper
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
				if os.path.isfile(args.i):
					wallpaper.generate_theme(args.i)
				elif os.path.isdir(args.i):
					images = get_dir_imgs(args.i)
					for image in images:
						wallpaper.generate_theme(os.path.join(args.i, image))
				sys.exit(0)
			else:
				if os.path.isfile(args.i):
					print("Applying theme...")
					wallpaper.apply_theme(args.i)
					
					if args.l:
						print("Applying as lockscreen...")
						LockscreenGenerate(args.i).update()

				elif os.path.isdir(args.i):
					image = get_random_image(args.i)
					print("Applying theme...")
					wallpaper.apply_theme(image) 

					if args.l:
						print("Applying as lockscreen...")
						LockscreenGenerate(image).update()
				sys.exit(0)
		elif args.p:
			if(os.path.isfile(os.path.join(CACHE_DESKTOP_PATH, "last"))):
				with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "r") as file:
					filedata = str(file.read()).rstrip()
					if(os.path.isfile(filedata)):
						print("Applying last used theme...")
						wallpaper.apply_theme(filedata)
						LockscreenGenerate(filedata).update()
						if args.l:
							print("Applying as lockscreen...")
					else:
						error_msg("Failed to load file")
						sys.exit(1)
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

def get_dir_imgs(img_dir):
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types)]

def get_random_image(img_dir):
	images = get_dir_imgs(img_dir) 
	random.shuffle(images)
	return os.path.join(img_dir, images[0])

def main():
	os.makedirs(CACHE_PATH, exist_ok=True)
	os.makedirs(CACHE_DESKTOP_PATH, exist_ok=True)
	os.makedirs(CACHE_LOCKSCREEN_PATH, exist_ok=True)
	os.makedirs(CONFIG_PATH, exist_ok=True)
	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()