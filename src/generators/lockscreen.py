import os
import subprocess
import shutil
import re
import random
import sys
from Xlib import X, display
from Xlib.ext import randr

from utils.settings import CACHE_LOCKSCREEN_PATH
from utils import utils

display_re = "([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)" # Regex to find the monitor resolutions

class LockscreenGenerate:
	def __init__(self, image):
		if os.path.isfile(image):
			self.image = [utils.get_image(image)]
		elif os.path.isdir(image):
			self.image = [utils.get_image(os.path.join(image, img)) for img in utils.get_dir_imgs(image)]
		else:
			print("File does not exist!")
			sys.exit(1)

		self.screen_md5 = utils.md5(subprocess.check_output(["xrandr"]))[:20]
		

	def generate(self):
		img_count = 0
		for image in self.image:
			img_count += 1
			tmp_imgs = []
			params = ""
			output_img_height=0
			output_img_width=0

			img_md5 = utils.md5_file(image)[:20]
			img_path = os.path.join(CACHE_LOCKSCREEN_PATH, img_md5 + "_" + self.screen_md5 + ".png")

			cmd = ['xrandr']
			p = subprocess.check_output(cmd)
 
			# Get all resolutions
			resolutions = re.findall(display_re,str(p))

			for resolution in resolutions:
				width, height, screen_x, screen_y = map(int, resolution)
				#print("Display: " + width + "x" + height + " \tx offset: " + screen_x + " \ty offset: " + screen_y)
				tmp_img = os.path.join(CACHE_LOCKSCREEN_PATH, "tmp_"+ str(width)+"x"+str(height)+"_"+img_md5)
				tmp_imgs.append(tmp_img)

				if not os.path.isfile(tmp_img):
					subprocess.run(["convert", image, '-resize', str(width) + "X" + str(height)+"^", '-gravity', 'Center', '-crop', str(width) + "X" + str(height) + "+0+0", '+repage', tmp_img])
				
				if output_img_width < width+screen_x:
					output_img_width = width+screen_x
				
				if output_img_height < height+screen_y:
					output_img_height = height+screen_y


				params = params + " " + tmp_img + " -geometry +" + str(screen_x) + "+" + str(screen_y) + " -composite -fill black -colorize 50% -blur 0x4"
			
			print("["+ str(img_count) + "/" + str(len(self.image)) + "] Generating lockscreen for: " + image + "...")

			subprocess.run(["convert", "-size", str(output_img_width)+"x"+str(output_img_height), "xc:rgb(1,0,0)", img_path])
			args = [["convert", img_path], params.split(" "), [img_path]]
			args = [y for x in args for y in x]
			while "" in args:
				args.remove("")
			subprocess.run(args)

			for file in tmp_imgs:
				os.remove(file)

	def update(self):
		images = self.image
		random.shuffle(images)
		image = images[0]

		img_md5 = utils.md5_file(image)[:20]
		img_path = os.path.join(CACHE_LOCKSCREEN_PATH, img_md5 + "_" + self.screen_md5 + ".png")

		if os.path.isfile(img_path):
			shutil.copyfile(img_path, os.path.join(CACHE_LOCKSCREEN_PATH, "lockscreen"))	
		else:
			self.generate()
			self.update()
