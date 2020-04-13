import unittest
from kadai import colorgen

class TestColorgen(unittest.TestCase):
	def test_color_output_length(self):
		result = colorgen.get("tests/assets/test.jpg")
		self.assertEqual(len(result), 16)

	def test_color_hex(self):
		result = colorgen.get("tests/assets/test.jpg")
		for color in result:
			hex_string = color[1:]
			int(hex_string, 16)
	
	def test_color_length(self):
		result = colorgen.get("tests/assets/test.jpg")
		for color in result:
			self.assertEqual(len(color), 7)

if __name__ == "__main__":
	unittest.main()