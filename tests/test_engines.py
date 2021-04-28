import unittest
from kadai.engine import vibrance, hue, base_engine, color_thief_engine, pastel
from kadai.utils import color_utils

test_image = "tests/assets/test.jpg"


class TestEngine(unittest.TestCase):
    def setUp(self):
        self._rgb = (255, 0, 0)
        self._color_list = (
            self._rgb,
            self._rgb,
            self._rgb,
            self._rgb,
            self._rgb,
            self._rgb,
            self._rgb,
        )


class TestBaseEngine(TestEngine):
    def setUp(self):
        super().setUp()
        self._engine = base_engine.BaseEngine(test_image)

    def test_generate(self):
        with self.assertRaises(NotImplementedError):
            self._engine.generate()

    def test_get_dominant_color(self):
        with self.assertRaises(NotImplementedError):
            self._engine.get_dominant_color()

    def test_get_palette(self):
        with self.assertRaises(TypeError):
            self._engine.get_palette()

    def test_make_palette(self):
        palette = self._engine._make_palette(
            self._color_list, (1, 0.9, 0.8, 0.7, 0.6, 0.5), (1, 0.9, 0.8)
        )
        self.assertEqual(len(palette), 16)


class TestBaseEngine_functions(unittest.TestCase):
    def test_modify_rgb_value_saturation(self):
        color = base_engine.modify_rgb_value_saturation((255, 0, 0), 0.5, 0.5)
        self.assertEqual(color, "#7f3f3f")


class TestColorThiefEngine(TestEngine):
    def setUp(self):
        self._engine = color_thief_engine.ColorThiefEngine(test_image)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertEqual(len(colors), 7)

    def test_get_dominant_color(self):
        color = self._engine.get_dominant_color()
        self.assertIsInstance(color, tuple)
        self.assertEqual(color, (128, 178, 178))


class TestHueEngine(TestEngine):
    def setUp(self):
        self._engine = hue.HueEngine(test_image)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertIsInstance(colors, list)
        self.assertEqual(len(colors), 7)


class TestHue_functions(unittest.TestCase):
    def setUp(self):
        self._color = (255, 0, 0)

    def test_generate_base_colors(self):
        colors = hue.generate_base_colors(self._color)
        self.assertIsInstance(colors, list)
        self.assertEqual(len(colors), 7)
        for color in colors:
            self.assertGreaterEqual(color_utils.rgb_to_hsv(color)[1], 0.4)

    def test_get_min_distance_hues(self):
        distance = float(hue.get_min_distance_hues((255, 100, 0)))
        self.assertAlmostEqual(distance, -0.065359477)


class TestPastelEngine(TestEngine):
    def setUp(self):
        super().setUp()
        self._engine = pastel.PastelEngine(test_image)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertEqual(len(colors), 7)
        self.assertIsInstance(colors, list)

    def test_get_palette(self):
        palette = self._engine.get_palette()
        self.assertEqual(len(palette), 2)
        self.assertIsInstance(palette, dict)
        self.assertEqual(len(palette["dark"]), 16)
        self.assertEqual(len(palette["light"]), 16)

    def test_get_dominant_color(self):
        color = self._engine.get_dominant_color()
        self.assertEqual(color, (153, 255, 255))


class TestVibranceEngine(TestEngine):
    def setUp(self):
        super().setUp()
        self._engine = vibrance.VibranceEngine(test_image)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertEqual(len(colors), 7)
        self.assertIsInstance(colors, list)


class TestVibrance_functions(unittest.TestCase):
    def test_calculate_vibrance(self):
        color_vibrance = vibrance.calculate_vibrance((200, 0, 0))
        self.assertAlmostEqual(color_vibrance, 0.94068627)

    def test_calculate_vibrance_with_list(self):
        colors = [(200, 0, 0), (100, 100, 100)]
        vibrances = vibrance.calculate_vibrance_with_list(colors)
        self.assertEqual(len(vibrances), 2)
        self.assertIsInstance(vibrances, list)
        for color_vibrance in vibrances:
            self.assertIn(color_vibrance[0], colors)
            self.assertLessEqual(color_vibrance[1], 1)
            self.assertGreaterEqual(color_vibrance[1], 0)

    def test_sort_by_vibrance(self):
        sorted_colors = vibrance.sort_by_vibrance([(10, 10, 0), (255, 100, 0)])
        self.assertIsInstance(sorted_colors, list)
        self.assertEqual(sorted_colors, [(255, 100, 0), (10, 10, 0)])


"""
class TestVibranceEngine(unittest.TestCase):
    def test_color_output_length(self):
        result = vibrance.VibranceEngine("tests/assets/test.jpg").generate()
        self.assertEqual(len(result), 7)

    def test_color_length(self):
        result = vibrance.VibranceEngine("tests/assets/test.jpg").generate()
        for color in result:
            self.assertEqual(len(color), 3)

    def test_get_image_brightness(self):
        brightness = vibrance.get_image_brightness("tests/assets/test.jpg")
        self.assertEqual(brightness, 44.200175908777595)

    def test_sort_by_vibrance(self):
        sorted_list = vibrance.sort_by_vibrance([(255, 0, 0), (200, 0, 0)])
        self.assertEqual(sorted_list, [(255, 0, 0), (200, 0, 0)])


class TestHueEngine(unittest.TestCase):
    def test_color_output_length(self):
        result = genhue.HueEngine("tests/assets/test.jpg").generate()
        self.assertEqual(len(result), 7)

    def test_color_length(self):
        result = genhue.HueEngine("tests/assets/test.jpg").generate()
        for color in result:
            self.assertEqual(len(color), 3)

    def test_generateBaseColors(self):
        base_colors = genhue.generateBaseColors((255, 0, 0))
        self.assertEqual(
            base_colors,
            [
                (0, 0, 255),
                (255, 0, 0),
                (0, 255, 0),
                (255, 255, 0),
                (0, 0, 255),
                (255, 0, 255),
                (0, 255, 255),
            ],
        )

    def test_getDominantColorFromImage(self):
        dominant_color = genhue.getDominantColorFromImage("tests/assets/test.jpg")
        self.assertEqual(dominant_color, (128, 178, 178))

    def test_shiftHuesByDistance(self):
        new_colors = genhue.shiftHuesByDistance([(255, 0, 0), (125, 0, 0)], 0.5)
        self.assertEqual(new_colors, [(0, 255, 255), (0, 125, 125)])
"""

if __name__ == "__main__":
    unittest.main()
