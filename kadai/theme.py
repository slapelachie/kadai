import sys
import os
import logging
import tqdm
import re
import json

from kadai import colorgen
from kadai import log
from kadai.utils import FileUtils
from kadai.settings import DEBUG_MODE

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
		md5_hash = images[i][1]

		if len([os.path.join(theme_dir, x.name) for x in os.scandir(theme_dir)\
			if md5_hash in x.name]) == 0:
			non_gen_images.append(images[i])

	return non_gen_images

def clear_and_write_data_to_file(file_path, data):
	if os.path.isfile(file_path):
		open(os.path.expanduser(file_path), 'w').close()
	with open(os.path.expanduser(file_path), 'a') as file:
		file.write(data)

def create_file_from_template(template_file, image_path, colors, out_path):
	filedata = template_file.read()

	# Change placeholder values
	filedata = filedata.replace("[wallpaper]", image_path)
	for i in range(len(colors)):
		filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
	
	clear_and_write_data_to_file(out_path, filedata)

def check_backend(backend):
	if not backend:
		return 'vibrance'
	else:
		return backend

def generate(images_path, out_dir, override=False, backend='vibrance'):
	""" Generates the theme passed on the parent class """
	backend = check_backend(backend)
	generate_images = []

	theme_dir = os.path.join(out_dir, 'themes/')
	FileUtils.ensure_output_dir_exists(theme_dir)

	images = [[i, FileUtils.md5_file(i)[:20]] for i in FileUtils.get_image_list(images_path)]
	template = os.path.join(os.path.abspath(os.path.dirname(__file__)),
		"data/template.json")

	generate_images = images if override else get_non_generated(images, theme_dir)

	# Recursively go through every image
	if len(generate_images) > 0:
		for i in tqdm.tqdm(range(len(generate_images))):
			image = generate_images[i][0]
			md5_hash = generate_images[i][1]
			out_file = os.path.join(theme_dir, md5_hash + '.json')
		
			# Generate the pallete
			colors = colorgen.generate(image, backend)

			tqdm_logger.log(15, "[" + str(i+1) + "/" + str(len(generate_images)) + "] Generating theme for " + image + "...")
		
			with open(template) as template_file:
				create_file_from_template(template_file, str(image), colors, out_file)
	else:
		logger.info("No themes to generate.")

def update(image, out_dir, template_dir, post_scripts=False):
	"""
	Updates the theme to the parsed image

	Arguments:
		lockscreen (bool) -- if the lockscreen should be generated
			default: False
	"""
	theme_dir = os.path.join(out_dir, 'themes/')
	FileUtils.ensure_output_dir_exists(theme_dir)

	# Get the md5 hash of the image
	md5_hash = FileUtils.md5_file(image)[:20]

	if not os.path.isfile(os.path.join(theme_dir, md5_hash+".json")):
		raise noPreGenThemeError("Theme file for this image does not exist!")

	with open(os.path.join(theme_dir, md5_hash + ".json")) as json_data:
		theme_data = json.load(json_data)

	colors = theme_data['colors']
	wallpaper = theme_data['wallpaper']

	templates = get_template_files(template_dir)

	# Applies values to the templates and concats into single theme file	
	for template in templates:
		template_path = os.path.join(template_dir, template)
		out_file = os.path.join(out_dir, template[:-5])
		with open(template_path) as template_file:
			filedata = template_file.read()

			# Change placeholder values
			for i in range(16):
				filedata = filedata.replace("[color" + str(i) + "]", str(colors['color'+str(i)]))

			filedata = filedata.replace("[background]", str(colors['color0']))
			filedata = filedata.replace("[background_light]", str(colors['color8']))
			filedata = filedata.replace("[foreground]", str(colors['color15']))
			filedata = filedata.replace("[foreground_dark]", str(colors['color7']))

			if os.path.isfile(out_file):
				open(os.path.expanduser(out_file), 'w').close()
			with open(os.path.expanduser(out_file), 'a') as file:
				file.write(filedata)

	# Link wallpaper to cache folder
	image_symlink = os.path.join(out_dir, 'image')
	if os.path.isfile(image_symlink):
		os.remove(image_symlink)
	os.symlink(wallpaper, image_symlink)

	# Run external scripts
	if post_scripts:
		FileUtils.run_post_scripts()
