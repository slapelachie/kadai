import unittest
import shutil
import os
from kadai import generate
from kadai.generate import ThemeGenerator

out_dir = '/tmp/github-runner-kadai/'
template_dir = 'tests/assets/templates'

class TestUtils(unittest.TestCase):
	def test_template_find(self):
		template_files = generate.get_template_files(template_dir)
		self.assertEqual(len(template_files), 2)
	
	def test_generate(self):
		shutil.rmtree(out_dir, ignore_errors='FileNotFoundError')
		ThemeGenerator('tests/assets/test.jpg', path=out_dir, quite=True).generate(template_dir=template_dir)
		print(os.listdir(out_dir))
		self.assertIs(os.path.isfile(os.path.join(out_dir, 'themes/74366ae1ada324257e36-colors.sh')), True)
		self.assertIs(os.path.isfile(os.path.join(out_dir, 'themes/74366ae1ada324257e36-Xdefaults')), True)

	def test_update(self):
		ThemeGenerator('tests/assets/test.jpg', path=out_dir, quite=True).update(post_scripts=False)
		self.assertIs(os.readlink(os.path.join(out_dir, 'colors.sh')) ==\
			os.path.join(out_dir, 'themes/74366ae1ada324257e36-colors.sh'), True)
		self.assertEqual(os.readlink(os.path.join(out_dir, 'Xdefaults')),
			os.path.join(out_dir, 'themes/74366ae1ada324257e36-Xdefaults'))


if __name__ == "__main__":
	unittest.main()