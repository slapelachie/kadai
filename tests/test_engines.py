import unittest
import warnings
from kadai.engine import vibrance, hue, base_engine, color_thief_engine, pastel
from kadai.utils import color_utils

TEST_IMAGE = "tests/assets/test.jpg"


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
        self._engine = base_engine.BaseEngine(TEST_IMAGE)

    def test_generate(self):
        with self.assertRaises(NotImplementedError):
            self._engine.generate()

    def test_get_dominant_color(self):
        with self.assertRaises(NotImplementedError):
            self._engine.get_dominant_color()

    def test_get_palette(self):
        with self.assertRaises(TypeError):
            self._engine.get_palette()


class TestColorThiefEngine(TestEngine):
    def setUp(self):
        self._engine = color_thief_engine.ColorThiefEngine(TEST_IMAGE)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertEqual(len(colors), 7)

    def test_gen_colors(self):
        warnings.warn("Test not implemented")

    def test_get_dominant_color(self):
        color = self._engine.get_dominant_color()
        self.assertIsInstance(color, tuple)
        self.assertEqual(color, (128, 178, 178))


class TestHueEngine(TestEngine):
    def setUp(self):
        self._engine = hue.HueEngine(TEST_IMAGE)

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

    def test_shift_hues_distance(self):
        warnings.warn("Test not implemented")

    def test_get_min_distance_hues(self):
        distance = float(hue.get_min_distance_hues((255, 100, 0)))
        self.assertAlmostEqual(distance, -0.065359477)


class TestPastelEngine(TestEngine):
    def setUp(self):
        super().setUp()
        self._engine = pastel.PastelEngine(TEST_IMAGE)

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
        self._engine = vibrance.VibranceEngine(TEST_IMAGE)

    def test_generate(self):
        colors = self._engine.generate()
        self.assertEqual(len(colors), 7)
        self.assertIsInstance(colors, list)


class TestVibrance_functions(unittest.TestCase):
    def test_sort_by_vibrance(self):
        sorted_colors = vibrance.sort_by_vibrance([(10, 10, 0), (255, 100, 0)])
        self.assertIsInstance(sorted_colors, list)
        self.assertEqual(sorted_colors, [(255, 100, 0), (10, 10, 0)])

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

    def test_sort_to_list(self):
        warnings.warn("Test not implemented")

    def test_sort_colors(self):
        warnings.warn("Test not implemented")


if __name__ == "__main__":
    unittest.main()
