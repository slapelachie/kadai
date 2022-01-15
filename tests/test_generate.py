import unittest
import warnings
import os
import shutil

from PIL import Image

from kadai import themer
from kadai.config_handler import ConfigHandler

OUT_DIR = "/tmp/github-runner-kadai/"
ASSETS_DIR = "tests/assets/"
config_path = os.path.join(ASSETS_DIR, "config.json")

config_handler = ConfigHandler()
config_handler.set_config_file_path(config_path)
config = config_handler.get_config()


class TestEngines(unittest.TestCase):
    def setUp(self):
        self._themer = themer.Themer(
            "tests/assets/test.jpg",
            config=config,
            run_hooks=False,
            out_path=OUT_DIR,
            cache_path=OUT_DIR,
        )

    def test_setget_override(self):
        self._themer.set_override(False)
        self.assertFalse(self._themer.get_override())

        self._themer.set_override(True)
        self.assertTrue(self._themer.get_override())

    def test_setget_run_hooks(self):
        self._themer.set_run_hooks(False)
        self.assertFalse(self._themer.get_run_hooks())

        self._themer.set_run_hooks(True)
        self.assertTrue(self._themer.get_run_hooks())

    def test_setget_display_progress(self):
        self._themer.set_display_progress(False)
        self.assertFalse(self._themer.get_display_progress())

        self._themer.set_display_progress(True)
        self.assertTrue(self._themer.get_display_progress())

    def test_setget_use_light_theme(self):
        self._themer.set_use_light_theme(False)
        self.assertFalse(self._themer.get_use_light_theme())

        self._themer.set_use_light_theme(True)
        self.assertTrue(self._themer.get_use_light_theme())

    def test_setget_engine_name(self):
        self._themer.set_engine_name("test123")
        self.assertEqual(self._themer.get_engine_name(), "test123")

    def test_setget_out_path(self):
        self._themer.set_out_path("/tmp")
        self.assertEqual(self._themer.get_out_path(), "/tmp")

    def test_setget_cache_path(self):
        self._themer.set_cache_path("/tmp")
        self.assertEqual(self._themer.get_cache_path(), "/tmp")

    def test_setget_user_template_path(self):
        self._themer.set_user_template_path("/tmp")
        self.assertEqual(self._themer.get_user_template_path(), "/tmp")

    def test_setget_user_hooks_path(self):
        self._themer.set_user_hooks_path("/tmp")
        self.assertEqual(self._themer.get_user_hooks_path(), "/tmp")

    def test_get_color_palette(self):
        warnings.warn("Test not implemented")

    def test_generate(self):
        warnings.warn("Test not implemented")

    def test_update(self):
        warnings.warn("Test not implemented")

    def test_get_engine(self):
        warnings.warn("Test not implemented")

    def test_get_template_files(self):
        # Test if can find all 2 template files
        template_files = themer.get_template_files(
            os.path.join(ASSETS_DIR, "templates/")
        )
        self.assertEqual(len(template_files), 2)

    def test_get_non_generated(self):
        warnings.warn("Test not implemented")

    def test_clear_write_data_to_file(self):
        warnings.warn("Test not implemented")

    def test_clear_write_json_to_file(self):
        warnings.warn("Test not implemented")

    def test_create_template_from_palette(self):
        warnings.warn("Test not implemented")

    def test_create_tmp_image(self):
        tmp_image_path = os.path.join(OUT_DIR, "test_create_tmp_image.jpg")
        themer.create_tmp_image(os.path.join(ASSETS_DIR, "test.jpg"), tmp_image_path)
        image = Image.open(tmp_image_path)
        self.assertEqual(image.size, (100, 50))
        self.assertEqual(image.mode, "RGB")

        os.remove(tmp_image_path)

    def test_modify_file_with_template(self):
        warnings.warn("Test not implemented")
        # file_data = """[color0], [background], [background_light], [foreground],\
        # [foreground_dark], [primary]"""
        # colors = {
        #    "color0": "#f00000",
        #    "color8": "#ff0000",
        #    "color15": "#fff000",
        #    "color7": "#ffff00",
        # }
        # primary_color = "#ffffff"

        # updated_data = themer.modify_file_with_template(
        #    file_data, colors, primary_color
        # )

        # self.assertEqual(updated_data, "{'color0': #ffffff, 'primary': #ff0000}")

    def test_symlink_image_path(self):
        symlink_out = os.path.join(OUT_DIR, "image")
        themer.symlink_image_path(os.path.join(ASSETS_DIR, "test.jpg"), OUT_DIR)

        self.assertTrue(os.path.islink(symlink_out))
        os.remove(symlink_out)

    def test_create_file_from_template(self):
        warnings.warn("Test not implemented")


if __name__ == "__main__":
    unittest.main()
