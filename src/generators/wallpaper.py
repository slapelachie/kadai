import sys
import os
import glob
import subprocess
import hashlib

from utils import colorgen
from utils import utils
from utils.settings import CACHE_DESKTOP_PATH, CONFIG_PATH

def apply_theme(img):
	image = utils.get_image(img)
	theme = generate_theme(img)
	# xdefaults = "#include \"" + theme + "\"\n"	

	with open(os.path.join(CACHE_DESKTOP_PATH, "last"), "w+") as file:
		file.write(image)

	subprocess.run(["xrdb", "-merge", os.path.expanduser(theme)])
	subprocess.run(["feh", "--bg-fill", image])
	subprocess.run(["i3-msg","restart"])
	subprocess.run(["spicetify","update"])
	subprocess.run(["convert", image, "-fill", "black", "-colorize", "70%", "-blur", "0x4",
		os.path.expanduser("~/.config/startpage/images/background")])

def generate_theme(img):
	image = utils.get_image(img)
	md5_hash = utils.md5(image)[:20]
	theme_path = os.path.join(CACHE_DESKTOP_PATH, md5_hash)

	if not os.path.isfile(theme_path):
		colors = colorgen.generate(image)

		print("Generating theme for " + image + "...")

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

	return theme_path