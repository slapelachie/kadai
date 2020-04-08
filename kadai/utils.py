import hashlib
import os
import re
import subprocess

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

def get_image(image):
	"""
	Get the absolute path of a passed file (image)

	Arguments:
		image (str) -- location of the file
	"""
	if os.path.isfile(image): 
		return os.path.abspath(image)

def get_dir_imgs(img_dir):
	"""
	Get a list of all images in a directory

	Arguments:
		img_dir (str) -- the directory where the images are stored
	"""
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types)]

def run_post_scripts(args=None):
	POST_SCRIPTS_DIR = os.path.join(DATA_PATH, 'postscripts')

	try:
		os.makedirs(POST_SCRIPTS_DIR, exist_ok=True)
	except:
		raise

	scripts = [f for f in os.listdir(POST_SCRIPTS_DIR) 
		if re.match(r'^([0-9]{2}-\w+)', f) 
			and os.access(os.path.join(POST_SCRIPTS_DIR, f), os.X_OK)]
	scripts.sort()

		
	for script in scripts:
		script = os.path.join(POST_SCRIPTS_DIR, script)

		# If arguments are passed
		if args:
			# Flatten the array to one dimension
			script = [[script], args.split(" ")]
			script = [y for x in script for y in x]

		subprocess.run(script)
