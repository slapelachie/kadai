import sys
import os
import glob
import subprocess
import hashlib
import random

from utils import colorgen
from utils import utils
from utils.settings import CACHE_DESKTOP_PATH, CONFIG_PATH
from generators.lockscreen import LockscreenGenerate

class ThemeGenerator:
	def __init__(self, image):
		if os.path.isfile(image):
			self.image = [utils.get_image(image)]
		elif os.path.isdir(image):
			self.image = [utils.get_image(os.path.join(image, img)) for img in utils.get_dir_imgs(image)]
		else:
			print("File does not exist!")
			sys.exit(1)

	def update(self, lockscreen):
		images = self.image
		random.shuffle(images)
		image = images[0]
		self.image = [image]
		md5_hash = utils.md5(image)[:20]
		theme_path = os.path.join(CACHE_DESKTOP_PATH, md5_hash)

		if not os.path.isfile(theme_path):
			self.generate()
			
		if lockscreen:
			LockscreenGenerate(image).update()

		with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "w+") as file:
			file.write(image)	

		subprocess.run(["xrdb", "-merge", os.path.expanduser(theme_path)])
		subprocess.run(["feh", "--bg-fill", image])
		subprocess.run(["i3-msg","restart"])
		subprocess.run(["spicetify","update"])
		subprocess.run(["convert", image, "-fill", "black", "-colorize", "70%", "-blur", "0x4",
			os.path.expanduser("~/.config/startpage/images/background")])

	def generate(self):
		img_count = 0
		for image in self.image:
			img_count += 1
			image = utils.get_image(image)
			md5_hash = utils.md5(image)[:20]
			theme_path = os.path.join(CACHE_DESKTOP_PATH, md5_hash)

			if not os.path.isfile(theme_path):
				colors = colorgen.generate(image)

				print("[" + str(img_count) + "/" + str(len(self.image)) + "] Generating theme for " + image + "...")

				templates = glob.glob(os.path.join(CONFIG_PATH, "templates/*"))
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