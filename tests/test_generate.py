import unittest
import shutil
import os
from kadai.utils import FileUtils
from kadai.themer import themer

out_dir = '/tmp/github-runner-kadai/'
template_dir = 'tests/assets/templates'

class TestUtils(unittest.TestCase):
	def test_template_find(self):
		# Test if can find all 2 template files
		template_files = themer.get_template_files(template_dir)
		self.assertEqual(len(template_files), 2)
	
	def test_generate_one(self):
		# Testing for generating one theme
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')

		generator = themer.Themer('tests/assets/test.jpg', out_dir)
		generator.generate()

		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55.json')), True)
		self.assertIs(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55.json')), True)

	def test_generate_all(self):
		# Testing for generating all images into themes
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')

		generator = themer.Themer('tests/assets/', out_dir)
		generator.generate()

		self.assertTrue(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55.json')))
		self.assertTrue(os.path.isfile(os.path.join(out_dir,
			'themes/31084f2c8577234aeb55.json')))

	def test_update(self):
		# Test if update passes when theme file exists
		generator = themer.Themer('tests/assets/test.jpg', out_dir)
		generator.setRunPostScripts(False)
		generator.setUserTemplatePath(template_dir)
		generator.update()
		#theme.update('tests/assets/test.jpg', out_dir, template_dir)
		
		self.assertTrue(os.path.isfile(os.path.join(out_dir,
			'colors.sh')))
		self.assertTrue(os.path.isfile(os.path.join(out_dir,
			'Xdefaults')))
	
	def test_update_fail(self):
		# Test if fail if theme file does not exist
		generator = themer.Themer('tests/assets/test.jpg', out_dir)
		generator.setRunPostScripts(False)
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')
		try:
			generator.update()
			#theme.update('tests/assets/test.jpg', out_dir, template_dir)
			raise ValueError("Passed Succesfully?!")
		except FileUtils.noPreGenThemeError:
			pass


if __name__ == "__main__":
	unittest.main()