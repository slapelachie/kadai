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

from colorgen import ColorGen

cache_path = os.path.expanduser('~/.cache/kadai')
config_path = os.path.expanduser('~/.config/kadai')

def error_msg(msg):
	print("[ERROR]: " + msg)

def get_args():
	arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")

	arg.add_argument("-p", action="store_true",
		help="Use last set theme")

	arg.add_argument("-i", metavar="\"path/to/dir\"",
			help="the input file")

	arg.add_argument("-g", action="store_true",
			help="generate themes")

	arg.add_argument("-l", action="store_true",
			help="generate and apply lockscreen")

	return arg

def parse_args(parser):
	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		sys.exit(1)

	if args.i:
		if args.g:
			if os.path.isfile(args.i):
				generate_theme(args.i)
			elif os.path.isdir(args.i):
				images = get_dir_imgs(args.i)
				for image in images:
					generate_theme(os.path.join(args.i, image))
			sys.exit(0)
		else:
			if os.path.isfile(args.i):
				print("Applying theme...")
				apply_theme(args.i)
				
				if args.l:
					print("Applying as lockscreen...")
					subprocess.run(["lockscreen-gen", "-i", args.i])

			elif os.path.isdir(args.i):
				image = get_random_image(args.i)
				print("Applying theme...")
				apply_theme(image) 

				if args.l:
					print("Applying as lockscreen...")
					subprocess.run(["lockscreen-gen", "-i", image])
			sys.exit(0)
	elif args.p:
		if(os.path.isfile(os.path.join(cache_path, "last"))):
			with open(os.path.join(cache_path, "last"), "r") as file:
				filedata = str(file.read()).rstrip()
				if(os.path.isfile(filedata)):
					print("Applying last used theme...")
					apply_theme(filedata)
				
					if args.l:
						print("Applying as lockscreen...")
						subprocess.run(["lockscreen-gen", "-i", filedata])
				else:
					error_msg("Failed to load file")
					sys.exit(1)
		else:
			error_msg("Last file does not exist!")
			sys.exit(1)
	else:
		error_msg("No file specified...")
		sys.exit(1)

 
def apply_theme(img):
	image = get_image(img)
	theme = generate_theme(img)
	# xdefaults = "#include \"" + theme + "\"\n"	

	with open(os.path.join(cache_path, "last"), "w+") as file:
		file.write(image)

	subprocess.run(["xrdb", "-merge", os.path.expanduser(theme)])
	subprocess.run(["feh", "--bg-fill", image])
	subprocess.run(["i3-msg","restart"])
	subprocess.run(["spicetify","update"])
	subprocess.run(["convert", image, "-fill", "black", "-colorize", "70%", "-blur", "0x4",
		os.path.expanduser("~/.config/startpage/images/background")])

def generate_theme(img):
	image = get_image(img)
	md5_hash = md5(image)[:20]
	theme_path = os.path.join(cache_path, md5_hash)

	if not os.path.isfile(theme_path):
		colors = ColorGen.generate(image)

		print("Generating theme for " + image + "...")

		templates = glob.glob(os.path.join(config_path, "templates/*"))
		open(os.path.expanduser(theme_path), 'w').close()

		for template in templates:
			with open(template) as file:
				filedata = file.read()

				for i in range(len(colors)):
					filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
				filedata = filedata.replace("[background]", str(colors[0]))
				filedata = filedata.replace("[foreground]", str(colors[7]))
				filedata = filedata.replace("[foreground_dark]", str(colors[15]))

				with open(os.path.expanduser(theme_path), 'a') as file:
  					file.write("\n"+ filedata + "\n")	

	return theme_path

def get_image(image):
	if os.path.isfile(image): 
		return os.path.abspath(image)

	sys.exit(1)

def get_dir_imgs(img_dir):
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types)]

def get_random_image(img_dir):
	images = get_dir_imgs(img_dir) 
	random.shuffle(images)
	return os.path.join(img_dir, images[0])

def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def main():
	os.makedirs(cache_path, exist_ok=True)
	os.makedirs(config_path, exist_ok=True)
	parser = get_args()
	parse_args(parser)

if __name__ == "__main__":
	main()