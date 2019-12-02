import hashlib
import os

def md5(string):
	hash_md5 = hashlib.md5(str(string).encode())
	return hash_md5.hexdigest()

def md5_file(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def get_image(image):
	if os.path.isfile(image): 
		return os.path.abspath(image)