import unittest
from kadai.utils import file_utils, color_utils


class TestFileUtils(unittest.TestCase):
    def test_md5_string(self):
        md5 = file_utils.md5("test string")
        self.assertEqual(md5, "6f8db599de986fab7a21625b7916589c")

    def test_md5_file(self):
        file_md5 = file_utils.md5_file("tests/assets/test.jpg")
        self.assertEqual(file_md5, "31084f2c8577234aeb5563b95a2786a8")

    def test_check_if_image(self):
        self.assertTrue(file_utils.check_if_image("tests/assets/test.jpg"))
        self.assertFalse(file_utils.check_if_image("tests/assets/test.txt"))

    def test_get_dir_images(self):
        images = file_utils.get_dir_imgs("tests/assets/")
        self.assertEqual(len(images), 1)

    def test_get_image_list_one(self):
        images = file_utils.get_image_list("tests/assets/test.jpg")
        self.assertEqual(len(images), 1)

    def test_get_image_list_one_fail(self):
        with self.assertRaises(ValueError):
            file_utils.get_image_list("tests/assets/test.txt")

    def test_get_image_list_all(self):
        images = file_utils.get_image_list("tests/assets/")
        self.assertEqual(len(images), 1)

    def test_get_image_list_none(self):
        with self.assertRaises(FileNotFoundError):
            file_utils.get_image_list("tests/")

    def test_get_hooks(self):
        scripts = file_utils.get_hooks(hooks_dir="tests/assets/hooks/")
        self.assertEqual(len(scripts), 1)


class TestColorUtils(unittest.TestCase):
    def setUp(self):
        self._rgb = (255, 0, 0)
        self._hex = "#ff0000"
        self._hsv = (0, 1, 1)

    def test_rgb_to_hex(self):
        hex = color_utils.rgb_to_hex(self._rgb)
        self.assertEqual(hex, self._hex)

    def test_hex_to_rgb(self):
        rgb = color_utils.hex_to_rgb(self._hex)
        self.assertEqual(rgb, self._rgb)

    def test_rgb_to_hsv(self):
        hsv = color_utils.rgb_to_hsv(self._rgb)
        self.assertEqual(hsv, self._hsv)

    def test_hsv_to_rgb(self):
        rgb = color_utils.hsv_to_rgb((0, 1, 1))
        self.assertEqual(rgb, (255, 0, 0))

    def test_changeHsvValue(self):
        hsv = color_utils.change_hsv_value(self._hsv, 0.5)
        self.assertEqual(hsv, (0, 1, 0.5))

    def test_changeHsvHue(self):
        hsv = color_utils.change_hsv_hue(self._hsv, 0.5)
        self.assertEqual(hsv, (0.5, 1, 1))

    def test_changeHsvSaturation(self):
        hsv = color_utils.change_hsv_saturation(self._hsv, 0.5)
        self.assertEqual(hsv, (0, 0.5, 1))

    def test_changeHueFromRGB(self):
        rgb = color_utils.change_rgb_hue(self._rgb, 0.5)
        self.assertEqual(rgb, (0, 255, 255))

    def test_changeValueFromRGB(self):
        rgb = color_utils.change_rgb_value(self._rgb, 0.5)
        self.assertEqual(rgb, (127, 0, 0))

    def test_changeSaturationFromRGB(self):
        rgb = color_utils.change_rgb_saturation(self._rgb, 0.5)
        self.assertEqual(rgb, (255, 127, 127))

    def test_getHueFromRGB(self):
        hue = color_utils.get_rgb_hue(self._rgb)
        self.assertEqual(hue, 0)


if __name__ == "__main__":
    unittest.main()
