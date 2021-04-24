import unittest
import os
import shutil

from kadai import config_handler
from kadai.config_handler import ConfigHandler

out_dir = "/tmp/github-runner-kadai/"


class TestConfigHandler(unittest.TestCase):
    def setUp(self):
        self._configHandler = ConfigHandler()
        self._configHandler.set_config_path("tests/assets/non_config.json")

    def test_get_length(self):
        self.assertEqual(len(self._configHandler.get()), 6)

        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

    def test_save(self):
        self._configHandler.set_config_file_out_path(
            os.path.join(out_dir, "config.json")
        )
        self._configHandler.save()

        self.assertTrue(os.path.isfile(os.path.join(out_dir, "config.json")))

        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

    def test_load(self):
        self._configHandler.load("tests/assets/config.json")

        self.assertEqual(self._configHandler.get()["light_theme"], False)

    def test_compare_flag_with_config(self):
        config = self._configHandler.get()
        self.assertTrue(config_handler.compare_flag_with_config(True, config["light"]))
        self.assertFalse(
            config_handler.compare_flag_with_config(False, config["light"])
        )
