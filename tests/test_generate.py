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
		ThemeGenerator('tests/assets/test.jpg', out_dir, template_dir, quite=True).generate()
		print(os.listdir(os.path.join(out_dir, 'themes/')))
		self.assertIs(os.path.isfile(os.path.join(out_dir, 'themes/31084f2c8577234aeb55-colors.sh')), True)
		self.assertIs(os.path.isfile(os.path.join(out_dir, 'themes/31084f2c8577234aeb55-Xdefaults')), True)

	def test_update(self):
		ThemeGenerator('tests/assets/test.jpg', out_dir, template_dir, quite=True).update(post_scripts=False)
		self.assertIs(os.readlink(os.path.join(out_dir, 'colors.sh')) ==\
			os.path.join(out_dir, 'themes/31084f2c8577234aeb55-colors.sh'), True)
		self.assertEqual(os.readlink(os.path.join(out_dir, 'Xdefaults')),
			os.path.join(out_dir, 'themes/31084f2c8577234aeb55-Xdefaults'))


if __name__ == "__main__":
	unittest.main()