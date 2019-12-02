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

def get_dir_imgs(img_dir):
	file_types = ("png", "jpg", "jpeg")
	return [img.name for img in os.scandir(img_dir)
			if img.name.lower().endswith(file_types)]