import unittest
import shutil
import os
from kadai import theme, utils

out_dir = '/tmp/github-runner-kadai/'
template_dir = 'tests/assets/templates'

class TestUtils(unittest.TestCase):
	def test_template_find(self):
		# Test if can find all 2 template files
		template_files = theme.get_template_files(template_dir)
		self.assertEqual(len(template_files), 2)
	
	def test_generate_one(self):
		# Testing for generating one theme
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')
		theme.generate('tests/assets/test.jpg', template_dir, out_dir)

		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55-colors.sh')), True)
		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55-Xdefaults')), True)

	def test_generate_all(self):
		# Testing for generating all images into themes
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')
		theme.generate('tests/assets/', template_dir, out_dir)

		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55-colors.sh')), True)
		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55-Xdefaults')), True)

	def test_update(self):
		# Test if update passes when theme file exists
		theme.update('tests/assets/test.jpg', out_dir)

		self.assertEqual(os.readlink(os.path.join(out_dir, 'colors.sh')),
			os.path.join(out_dir, 'themes/31084f2c8577234aeb55-colors.sh'))
		self.assertEqual(os.readlink(os.path.join(out_dir, 'Xdefaults')),
			os.path.join(out_dir, 'themes/31084f2c8577234aeb55-Xdefaults'))
	
	def test_update_fail(self):
		# Test if fail if theme file does not exist
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')
		try:
			theme.update('tests/assets/test.jpg', out_dir)
			raise ValueError("Passed Succesfully?!")
		except theme.noPreGenThemeError:
			pass


if __name__ == "__main__":
	unittest.main()