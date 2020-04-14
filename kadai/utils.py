import hashlib
import os
import re
import subprocess
from PIL import Image

from .settings import DATA_PATH

def md5(string):
	"""
	Generates a md5 hash based on the parsed string

	Arguments:
		string (str) -- a string to be encoded
	"""

	hash_md5 = hashlib.md5(str(string).encode())
	return hash_md5.hexdigest()

def md5_file(fname):
	"""
	Generates a md5 hash based on the file parsed

	Arguments:
		fname (str) -- location of the file ('/home/bob/pic.png')
	"""

	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def ensure_output_dir_exists(directory):
	try:
		os.makedirs(directory, exist_ok=True)
	except: raise

def get_image(image):
	"""
	Get the absolute path of a passed file (image)

	Arguments:
		image (str) -- location of the file
	"""
	if os.path.isfile(image): 
		return os.path.abspath(image)

def check_if_image(file):
	try:
		Image.open(file).verify()
		return True
	except:
		return False

def get_dir_imgs(img_dir):
	"""
	Get a list of all images in a directory

	Arguments:
		img_dir (str) -- the directory where the images are stored
	"""
	file_types = ("png", "jpg", "jpeg")
	return [os.path.join(img_dir, img.name) for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types) and check_if_image(os.path.join(img_dir, img.name))]

def get_image_list(image_path):
	image_path = os.path.expanduser(image_path)
	if os.path.isfile(image_path):
		if(check_if_image(image_path)):
			return [get_image(image_path)]
		else:
			raise "Specified file is not an image!"
	elif os.path.isdir(image_path):
		images = get_dir_imgs(image_path)
		if len(images) == 0:
			raise "Specified directory does not contain any images!"

		return images
	else:
		raise ValueError("Unknown file type!")


def get_post_scripts(post_scripts_dir=os.path.join(DATA_PATH, 'postscripts')):
	try:
		os.makedirs(post_scripts_dir, exist_ok=True)
	except:
		raise

	scripts = [f for f in os.listdir(post_scripts_dir) 
		if re.match(r'^([0-9]{2}-\w+)', f) 
			and os.access(os.path.join(post_scripts_dir, f), os.X_OK)]
	scripts.sort()
	return scripts

def run_post_scripts(args=None, post_scripts_dir=os.path.join(DATA_PATH, 'postscripts')):		
	scripts = get_post_scripts(post_scripts_dir)

	for script in scripts:
		script = os.path.join(post_scripts_dir, script)

		# If arguments are passed
		if args:
			# Flatten the array to one dimension
			script = [[script], args]
			script = [y for x in script for y in x]

		with open(os.devnull, 'w') as devnull:
			subprocess.run(script, stdout=devnull, stderr=subprocess.STDOUT)
