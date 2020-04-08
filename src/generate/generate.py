import sys
import os
import glob
import subprocess
import hashlib
import random
import logging
import tqdm

from utils import colorgen
from utils import utils, log
from utils.settings import CACHE_PATH, DATA_PATH, DEBUG_MODE

logger = log.setup_logger(__name__+'.default', logging.INFO, log.defaultLoggingHandler())
tqdm_logger = log.setup_logger(__name__+'.tqdm', logging.INFO, log.TqdmLoggingHandler())

theme_dir = os.path.join(CACHE_PATH, "themes")
try:
	os.makedirs(theme_dir, exist_ok=True)
except: raise

class ThemeGenerator:
	"""
	Main class for generating themes

	Arguments:
		image (str) -- location of the image
	"""

	def __init__(self, image, verbose=False):
		self.verbose = verbose
		if DEBUG_MODE:
			logger.setLevel(logging.DEBUG)
			tqdm_logger.setLevel(logging.DEBUG)
		elif verbose:
			logger.setLevel(15)
			tqdm_logger.setLevel(15)

		# If the path is a file, get the image and set itself to that
		if os.path.isfile(image):
			logger.debug('Passed source is a file')
			self.image = [utils.get_image(image)]
		# If the path is a directory, get all images in it and get its absolute path
		elif os.path.isdir(image):
			logger.debug('Passed source is a directory')
			self.image = [utils.get_image(os.path.join(image, img)) for img in utils.get_dir_imgs(image)]
		else:
			logger.critical("File does not exist! Exiting...")
			sys.exit(1)

	def update(self):
		"""
		Updates the theme to the parsed image

		Arguments:
			lockscreen (bool) -- if the lockscreen should be generated
				default: False
		"""

		# Get a random image from the list of images
		images = self.image
		random.shuffle(images)
		image = images[0]
		self.image = [image]
		logger.debug("Set image to %s", image)

		# Get the md5 hash of the image
		md5_hash = utils.md5(image)[:20]
		logger.debug("Hash for %s is %s", image, md5_hash)
		# Set the path for the theme
		theme_path = os.path.join(theme_dir, md5_hash)
		logger.debug("Set output for theme to %s", theme_path)

		# If the theme doesn't exist, generate it
		if not os.path.isfile(theme_path):
			logger.debug("Theme does not exist, generating...")
			self.generate()
			
		# Update a file with the directory to the last image used
		with open(os.path.join(CACHE_PATH, "last"), "w+") as file:
			logger.debug("Updating last image to %s", image)
			file.write(image)	

		symlink_path = os.path.join(theme_dir, 'current_theme')

		if os.path.isfile(symlink_path):
			os.remove(symlink_path)

		os.symlink(theme_path, symlink_path)

		# Other programs that need to be updated for the change to occur
		logger.debug("Merging Xresources...")
		subprocess.run(["xrdb", "-merge", os.path.expanduser(theme_path)])

		# Run external scripts
		utils.run_post_scripts('theme', image)

	def generate(self, override=False):
		""" Generates the theme passed on the parent class """
		non_gen_imgs = []

		# Get all templates in the templates folder
		logger.debug("Searching recursively for templates under %s", os.path.join(DATA_PATH, "templates"))
		templates = glob.glob(os.path.join(DATA_PATH, "templates/*"))

		if len(templates) == 0:
			logger.warn("No template files found under %s, this will lead to theme files being blank!",
				os.path.join(DATA_PATH, "templates"))

		# Recursively go through every image
		logger.debug("Starting recursive file generation...")
		for i in range(len(self.image)):
			image = self.image[i]
			image = utils.get_image(image)
			md5_hash = utils.md5(image)[:20]
			theme_path = os.path.join(theme_dir, md5_hash)

			if not os.path.isfile(theme_path) or override:
				non_gen_imgs.append([image, theme_path])
		
		if len(non_gen_imgs) > 0:
			logger.info('Generating themes...')
			for i in tqdm.tqdm(range(len(non_gen_imgs))):
				image = non_gen_imgs[i][0]
				theme_path = non_gen_imgs[i][1]
			
				# If the theme file does not already exist, generate it
				tqdm_logger.debug("Generating theme file %s", theme_path)
				# Generate the pallete
				tqdm_logger.debug("Getting color pallete...")
				colors = colorgen.generate(image)

				tqdm_logger.log(15, "[" + str(i+1) + "/" + str(len(self.image)) + "] Generating theme for " + image + "...")

				tqdm_logger.debug("Clearing the theme file...")
				open(os.path.expanduser(theme_path), 'w').close()

				# Applies values to the templates and concats into single theme file	
				for template in templates:
					tqdm_logger.debug("Adding %s template to theme file", template)
					with open(template) as file:
						filedata = file.read()

						# Change placeholder values
						tqdm_logger.debug("Replacing template values from %s for real values...", template)
						for i in range(len(colors)):
							filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
						filedata = filedata.replace("[background]", str(colors[0]))
						filedata = filedata.replace("[foreground]", str(colors[7]))
						filedata = filedata.replace("[foreground_dark]", str(colors[15]))

						# Write to the theme file
						tqdm_logger.debug("Writing updated template file from %s to theme file %s", template, theme_path)
						with open(os.path.expanduser(theme_path), 'a') as file:
							file.write("\n"+ filedata + "\n")	
		else:
			logger.info("No themes to generate.")