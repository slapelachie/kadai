import sys
import os
import glob
import subprocess
import hashlib
import random
import logging
import tqdm

from utils import colorgen
from utils import utils
from utils.settings import CACHE_DESKTOP_PATH, CONFIG_PATH
from generators.lockscreen import LockscreenGenerate

log = logging.getLogger()

class ThemeGenerator:
	"""
	Main class for generating themes

	Arguments:
		image (str) -- location of the image
	"""

	def __init__(self, image):
		# If the path is a file, get the image and set itself to that
		if os.path.isfile(image):
			self.image = [utils.get_image(image)]
		# If the path is a directory, get all images in it and get its absolute path
		elif os.path.isdir(image):
			self.image = [utils.get_image(os.path.join(image, img)) for img in utils.get_dir_imgs(image)]
		else:
			logging.critical("File does not exist!")
			sys.exit(1)

	def update(self, lockscreen=False):
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

		# Get the md5 hash of the image
		md5_hash = utils.md5(image)[:20]
		# Set the path for the theme
		theme_path = os.path.join(CACHE_DESKTOP_PATH, md5_hash)

		# If the theme doesn't exist, generate it
		if not os.path.isfile(theme_path):
			self.generate()
			
		# If this is true, updates the lockscreen to the same image
		if lockscreen:
			LockscreenGenerate(image).update()

		# Update a file with the directory to the last image used
		with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "w+") as file:
			file.write(image)	

		# Other programs that need to be updated for the change to occur
		subprocess.run(["xrdb", "-merge", os.path.expanduser(theme_path)])
		subprocess.run(["feh", "--bg-fill", image])
		subprocess.run(["i3-msg","restart"])
		# Optional progarams
		# subprocess.run(["killall", "-USR1", "st"])
		subprocess.run(["spicetify","update"])
		subprocess.run(["convert", image, "-fill", "black", "-colorize", "70%", "-blur", "0x4",
			os.path.expanduser("~/.config/startpage/images/background")])

	def generate(self):
		""" Generates the theme passed on the parent class """
		logging.info('Generating themes...')
		# Recursively go through every image
		
		for i in tqdm.tqdm(range(len(self.image))):
			image = self.image[i]
			image = utils.get_image(image)
			md5_hash = utils.md5(image)[:20]
			theme_path = os.path.join(CACHE_DESKTOP_PATH, md5_hash)

			# If the theme file does not already exist, generate it
			if not os.path.isfile(theme_path):
				# Generate the pallete
				colors = colorgen.generate(image)

				log.log(15, "[" + str(i+1) + "/" + str(len(self.image)) + "] Generating theme for " + image + "...")

				# Get all templates in the templates folder
				templates = glob.glob(os.path.join(CONFIG_PATH, "templates/*"))
				open(os.path.expanduser(theme_path), 'w').close()

				# Applies values to the templates and concats into single theme file
				for template in templates:
					with open(template) as file:
						filedata = file.read()

						# Change placeholder values
						for i in range(len(colors)):
							filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
						filedata = filedata.replace("[background]", str(colors[0]))
						filedata = filedata.replace("[foreground]", str(colors[7]))
						filedata = filedata.replace("[foreground_dark]", str(colors[15]))

						# Write to the theme file
						with open(os.path.expanduser(theme_path), 'a') as file:
							file.write("\n"+ filedata + "\n")	