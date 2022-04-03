import unittest
import os
import shutil
import warnings

from kadai import config_handler
from kadai.config_handler import ConfigHandler

OUT_DIR = "/tmp/github-runner-kadai/"


class TestConfigHandler(unittest.TestCase):
    def setUp(self):
        self._config_handler = ConfigHandler()
        self._config_handler.set_config_file_path("tests/assets/non_config.json")

    def test_setget_config_file_path(self):
        self._config_handler.set_config_file_path("tests/assets/asdf.json")
        self.assertEqual(
            self._config_handler.get_config_file_path(), "tests/assets/asdf.json"
        )

    def test_setget_config_file_out_path(self):
        self._config_handler.set_config_file_out_path("tests/assets/asdf.json")
        self.assertEqual(
            self._config_handler.get_config_file_out_path(), "tests/assets/asdf.json"
        )

    def test_setget_config(self):
        # TODO: implement set test
        config = {"test123": False}
        self._config_handler.set_config(config)
        self.assertEqual(self._config_handler.get_config(), config)

    def test_setget_config_items(self):
        self.assertEqual(len(self._config_handler.get_config()), 8)

        shutil.rmtree(OUT_DIR, ignore_errors="FileNotFoundError")

    def test_save_load(self):
        config_out_path = os.path.join(OUT_DIR, "config.json")

        self._config_handler.set_config_file_out_path(config_out_path)

        config = self._config_handler.get_config()
        config["light"] = True

        self._config_handler.set_config(config)
        self._config_handler.save_config()

        self.assertTrue(os.path.isfile(config_out_path))

        self._config_handler.load_config(config_out_path)
        self.assertEqual(self._config_handler.get_config()["light"], True)

        shutil.rmtree(OUT_DIR, ignore_errors="FileNotFoundError")


class TestConfigHandlerFunctions(unittest.TestCase):
    def test_parse_config(self):
        warnings.warn("Test not implemented")
