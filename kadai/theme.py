import sys
import os
import logging
import tqdm
import re

from . import colorgen
from . import utils, log
from .settings import CACHE_PATH, DATA_PATH, DEBUG_MODE

class noPreGenThemeError(Exception):
	pass

logger = log.setup_logger(__name__+'.default', logging.INFO, log.defaultLoggingHandler())
tqdm_logger = log.setup_logger(__name__+'.tqdm', logging.INFO, log.TqdmLoggingHandler())

def get_template_files(template_dir):
	# Get all templates in the templates folder
	templates = [f for f in os.listdir(template_dir)
		if re.match(r'.*\.base$', f)]

	if len(templates) == 0:
		raise "No template files!"

	return templates

def get_non_generated(images, theme_dir):
	non_gen_images = []
	theme_dir = os.path.expanduser(theme_dir)
	for i in range(len(images)):
		image = images[i][0]
		md5_hash = images[i][1]

		if len([os.path.join(theme_dir, x.name) for x in os.scandir(theme_dir)\
			if md5_hash in x.name]) == 0:
			non_gen_images.append(images[i])

	return non_gen_images

def generate(images_path, template_dir, out_dir, override=False):
	""" Generates the theme passed on the parent class """
	generate_images = []

	theme_dir = os.path.join(out_dir, 'themes/')
	utils.ensure_output_dir_exists(theme_dir)

	images = [[i, utils.md5_file(i)] for i in utils.get_image_list(images_path)]
	templates = get_template_files(template_dir)

	generate_images = images if override else get_non_generated(images, theme_dir)

	# Recursively go through every image
	if len(generate_images) > 0:
		for i in tqdm.tqdm(range(len(generate_images))):
			image = generate_images[i][0]
			md5_hash = generate_images[i][1]
		
			# Generate the pallete
			colors = colorgen.generate(image)

			tqdm_logger.log(15, "[" + str(i+1) + "/" + str(len(generate_images)) + "] Generating theme for " + image + "...")

			# Applies values to the templates and concats into single theme file	
			for template in templates:
				template_path = os.path.join(template_dir, template)
				out_file = os.path.join(theme_dir, md5_hash + '-' + template[:-5])
				with open(template_path) as file:
					filedata = file.read()

					# Change placeholder values
					for i in range(len(colors)):
						filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
					filedata = filedata.replace("[background]", str(colors[0]))
					filedata = filedata.replace("[background_light]", str(colors[8]))
					filedata = filedata.replace("[foreground]", str(colors[15]))
					filedata = filedata.replace("[foreground_dark]", str(colors[7]))

					if os.path.isfile(out_file):
						open(os.path.expanduser(out_file), 'w').close()
					with open(os.path.expanduser(out_file), 'a') as file:
						file.write(filedata)
	else:
		logger.info("No themes to generate.")

def update(image, out_dir, post_scripts=False):
	"""
	Updates the theme to the parsed image

	Arguments:
		lockscreen (bool) -- if the lockscreen should be generated
			default: False
	"""
	theme_dir = os.path.join(out_dir, 'themes/')
	utils.ensure_output_dir_exists(theme_dir)

	# Get the md5 hash of the image
	md5_hash = utils.md5_file(image)[:20]

	theme_files = [f for f in os.listdir(theme_dir)
		if re.match(r'^' + md5_hash + r'-', f)]

	# If the theme doesn't exist, generate it
	if len(theme_files) == 0:
		raise noPreGenThemeError("Theme file for this image does not exist!")

	for theme in theme_files:
		theme_type = theme[21:]
		symlink_path = os.path.join(out_dir, theme_type)

		if os.path.isfile(symlink_path):
			os.remove(symlink_path)

		os.symlink(os.path.join(theme_dir, theme), symlink_path)

	# Link wallpaper to cache folder
	image_symlink = os.path.join(out_dir, 'image')
	if os.path.isfile(image_symlink):
		os.remove(image_symlink)
	os.symlink(image, image_symlink)


	# Run external scripts
	if post_scripts:
		utils.run_post_scripts([image])