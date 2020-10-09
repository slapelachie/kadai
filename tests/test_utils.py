import unittest
from kadai.utils import FileUtils,ColorUtils

class TestFileUtils(unittest.TestCase):
	def test_md5_string(self):
		md5 = FileUtils.md5('test string')
		self.assertEqual(md5, '6f8db599de986fab7a21625b7916589c')

	def test_md5_file(self):
		file_md5 = FileUtils.md5_file('tests/assets/test.jpg')
		self.assertEqual(file_md5, '31084f2c8577234aeb5563b95a2786a8')

	def test_check_if_image(self):
		self.assertTrue(FileUtils.check_if_image('tests/assets/test.jpg'))
		self.assertFalse(FileUtils.check_if_image('tests/assets/test.txt'))

	def test_get_dir_images(self):
		images = FileUtils.get_dir_imgs('tests/assets/')
		self.assertEqual(len(images), 1)	

	def test_get_image_list_one(self):
		images = FileUtils.get_image_list('tests/assets/test.jpg')
		self.assertEqual(len(images), 1)
		
	def test_get_image_list_one_fail(self):
		try:
			images = FileUtils.get_image_list('tests/assets/test.txt')
			raise ValueError("How!?")
		except:
			pass
	
	def test_get_image_list_all(self):
		images = FileUtils.get_image_list('tests/assets/')
		self.assertEqual(len(images), 1)

	def test_get_image_list_none(self):
		try:
			images = FileUtils.get_image_list('tests/')
			raise ValueError("How!?")
		except:
			pass

	def test_get_hooks(self):
		scripts = FileUtils.get_hooks(hooks_dir='tests/assets/hooks/')
		self.assertEqual(len(scripts), 1)

class TestColorUtils(unittest.TestCase):
	def test_rgb_to_hex(self):
		hex = ColorUtils.rgb_to_hex((255,0,0))
		self.assertEqual(hex, "#ff0000")

	def test_rgb_to_hsv(self):
		hsv = ColorUtils.rgb_to_hsv((255,0,0))
		self.assertEqual(hsv, (0,1,1))

	def test_hsv_to_rgb(self):
		rgb = ColorUtils.hsv_to_rgb((0,1,1))
		self.assertEqual(rgb, (255,0,0))

	def test_changeHsvValue(self):
		hsv = ColorUtils.changeHsvValue((0,1,1), 0.5)
		self.assertEqual(hsv, (0,1,0.5))

	def test_changeHsvHue(self):
		hsv = ColorUtils.changeHsvHue((0,1,1), 0.5)
		self.assertEqual(hsv, (0.5,1,1))

	def test_changeHsvSaturation(self):
		hsv = ColorUtils.changeHsvSaturation((0,1,1), 0.5)
		self.assertEqual(hsv, (0,0.5,1))

	def test_changeHueFromRGB(self):
		rgb = ColorUtils.changeHueFromRGB((255,0,0), 0.5)
		self.assertEqual(rgb, (0, 255, 255))

	def test_changeValueFromRGB(self):
		rgb = ColorUtils.changeValueFromRGB((255,0,0), 0.5)
		self.assertEqual(rgb, (127,0,0))

	def test_changeSaturationFromRGB(self):
		rgb = ColorUtils.changeSaturationFromRGB((255,0,0), 0.5)
		self.assertEqual(rgb, (255,127,127))

	def test_getHueFromRGB(self):
		hue = ColorUtils.getHueFromRGB((255,0,0))
		self.assertEqual(hue, 0)

if __name__ == "__main__":
	unittest.main()