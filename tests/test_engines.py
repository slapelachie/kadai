import unittest
from kadai.engine import vibrance,genhue

class TestVibranceEngine(unittest.TestCase):
	def test_color_output_length(self):
		result = vibrance.VibranceEngine("tests/assets/test.jpg").generate()
		self.assertEqual(len(result), 7)

	def test_color_length(self):
		result = vibrance.VibranceEngine("tests/assets/test.jpg").generate()
		for color in result:
			self.assertEqual(len(color), 3)

	def test_get_image_brightness(self):
		brightness = vibrance.get_image_brightness('tests/assets/test.jpg')
		self.assertEqual(brightness, 44.200175908777595)

	def test_sort_by_vibrance(self):
		sorted_list = vibrance.sort_by_vibrance([(255,0,0), (200,0,0)])
		self.assertEqual(sorted_list, [(255,0,0), (200,0,0)])

class TestHueEngine(unittest.TestCase):
	def test_color_output_length(self):
		result = genhue.HueEngine("tests/assets/test.jpg").generate()
		self.assertEqual(len(result), 7)
	
	def test_color_length(self):
		result = genhue.HueEngine("tests/assets/test.jpg").generate()
		for color in result:
			self.assertEqual(len(color), 3)

	def test_generateBaseColors(self):
		base_colors = genhue.generateBaseColors((255,0,0))
		self.assertEqual(base_colors, [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)])

	def test_getDominantColorFromImage(self):
		dominant_color = genhue.getDominantColorFromImage("tests/assets/test.jpg")
		self.assertEqual(dominant_color, (128,178,178))

	def test_shiftHuesByDistance(self):
		new_colors = genhue.shiftHuesByDistance([(255,0,0),(125,0,0)], .5)
		self.assertEqual(new_colors, [(0,255,255),(0,125,125)])

if __name__ == "__main__":
	unittest.main()