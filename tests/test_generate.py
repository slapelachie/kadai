import unittest
import shutil
import os
from kadai.utils import FileUtils
from kadai import themer

out_dir = '/tmp/github-runner-kadai/'
template_dir = 'tests/assets/templates'

class TestUtils(unittest.TestCase):
	def test_template_find(self):
		# Test if can find all 2 template files
		template_files = themer.get_template_files(template_dir)
		self.assertEqual(len(template_files), 2)


	def test_createValueSpreadDictionary(self):
		values = [0.1, 0.3, 0.5, 0.7, 0.9]
		pallete = themer.createValueSpreadDictionary(values, (255, 0, 0))
		self.assertEqual(pallete, {'0.1': '#190000', '0.3': '#4c0000', '0.5': '#7f0000', '0.7': '#b20000', '0.9': '#e50000'})

	def test_createValueColorPallete(self):
		colors = [(255,0,0), (0,255,0), (0,0,255)]
		pallete = themer.createValueColorPallete(colors)
		self.assertEqual(pallete, {'color0': {'0.1': '#190000', '0.3': '#4c0000', '0.5': '#7f0000', '0.7': '#b20000', '0.9': '#e50000'}, 'color1': {'0.1': '#001900', '0.3': '#004c00', '0.5': '#007f00', '0.7': '#00b200', '0.9': '#00e500'}, 'color2': {'0.1': '#000019', '0.3': '#00004c', '0.5': '#00007f', '0.7': '#0000b2', '0.9': '#0000e5'}})
	
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