import unittest
from kadai import utils

class TestUtils(unittest.TestCase):
	def test_md5_string(self):
		md5 = utils.md5('test string')
		self.assertEqual(md5, '6f8db599de986fab7a21625b7916589c')

	def test_md5_file(self):
		file_md5 = utils.md5_file('tests/assets/test.jpg')
		self.assertEqual(file_md5, '31084f2c8577234aeb5563b95a2786a8')

	def test_check_if_image(self):
		self.assertTrue(utils.check_if_image('tests/assets/test.jpg'))
		self.assertFalse(utils.check_if_image('tests/assets/test.txt'))

	def test_get_dir_images(self):
		images = utils.get_dir_imgs('tests/assets/')
		self.assertEqual(len(images), 1)	

	def test_get_image_list_one(self):
		images = utils.get_image_list('tests/assets/test.jpg')
		self.assertEqual(len(images), 1)
	
	def test_get_image_list_all(self):
		images = utils.get_image_list('tests/assets/')
		self.assertEqual(len(images), 1)

	def test_get_postscripts(self):
		scripts = utils.get_post_scripts(post_scripts_dir='tests/assets/postscripts/')
		self.assertEqual(len(scripts), 1)

if __name__ == "__main__":
	unittest.main()