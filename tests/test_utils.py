import unittest
from kadai.utils import file_utils, color_utils


class TestFileUtils(unittest.TestCase):
    def test_md5_string(self):
        md5 = file_utils.md5("test string")
        self.assertEqual(md5, "6f8db599de986fab7a21625b7916589c")

    def test_md5_file(self):
        file_md5 = file_utils.md5_file("tests/assets/test.jpg")
        self.assertEqual(file_md5, "31084f2c8577234aeb5563b95a2786a8")

    def test_get_directory_images(self):
        images = file_utils.get_directory_images("tests/assets/")
        self.assertEqual(len(images), 3)

    def test_get_image_list_one(self):
        images = file_utils.get_image_list("tests/assets/test.jpg")
        self.assertEqual(len(images), 1)

    def test_get_image_list_one_fail(self):
        with self.assertRaises(ValueError):
            file_utils.get_image_list("tests/assets/test.txt")

    def test_get_image_list_all(self):
        images = file_utils.get_image_list("tests/assets/")
        self.assertEqual(len(images), 3)

    def test_get_image_list_none(self):
        with self.assertRaises(FileNotFoundError):
            file_utils.get_image_list("tests/")

    def test_get_hooks(self):
        scripts = file_utils.get_hooks(hooks_directory="tests/assets/hooks/")
        self.assertEqual(len(scripts), 1)


class TestColorUtils(unittest.TestCase):
    def setUp(self):
        self._rgb = (255, 0, 0)
        self._hex = "#ff0000"
        self._hsv = (0, 1, 1)
        self._color_list = (
            (0, 0, 0),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 255, 255),
        )

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

    def test_chage_hsv_color(self):
        hsv = color_utils.change_hsv_value(self._hsv, 0.5)
        self.assertEqual(hsv, (0, 1, 0.5))

    def test_change_hsv_hue(self):
        hsv = color_utils.change_hsv_hue(self._hsv, 2)
        self.assertEqual(hsv, (2, 1, 1))

    def test_change_hsv_saturation(self):
        hsv = color_utils.change_hsv_saturation(self._hsv, 0.5)
        self.assertEqual(hsv, (0, 0.5, 1))

    def test_change_hsv_value(self):
        hsv = color_utils.change_hsv_hue(self._hsv, 0.5)
        self.assertEqual(hsv, (0.5, 1, 1))

    def test_change_rgb_hue(self):
        rgb = color_utils.change_rgb_hue(self._rgb, 0.5)
        self.assertEqual(rgb, (0, 255, 255))

    def test_change_rgb_saturation(self):
        rgb = color_utils.change_rgb_saturation(self._rgb, 0.5)
        self.assertEqual(rgb, (255, 127, 127))

    def test_change_rgb_value(self):
        rgb = color_utils.change_rgb_value(self._rgb, 0.5)
        self.assertEqual(rgb, (127, 0, 0))

    def test_get_rgb_hue(self):
        hue = color_utils.get_rgb_hue(self._rgb)
        self.assertEqual(hue, 0)

    def test_make_palette(self):
        palette = color_utils.make_palette(
            self._color_list, (1, 0.9, 0.8, 0.7, 0.6, 0.5), (1, 0.9, 0.8)
        )
        self.assertEqual(len(palette), 16)
        self.assertEqual(
            palette,
            {
                "color0": "#ff0000",
                "color7": "#e51616",
                "color8": "#cc0000",
                "color15": "#b21111",
                "color1": "#991e1e",
                "color9": "#7f1919",
                "color2": "#1e991e",
                "color10": "#197f19",
                "color3": "#1e1e99",
                "color11": "#19197f",
                "color4": "#99991e",
                "color12": "#7f7f19",
                "color5": "#1e9999",
                "color13": "#197f7f",
                "color6": "#991e1e",
                "color14": "#7f1919",
            },
        )

    def test_modify_rgb_value_saturation(self):
        color = color_utils.modify_rgb_value_saturation((255, 0, 0), 0.5, 0.5)
        self.assertEqual(color, "#7f3f3f")


if __name__ == "__main__":
    unittest.main()
