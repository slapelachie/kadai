import unittest
import os
import shutil
from kadai import config_handler
from kadai.config_handler import ConfigHandler

out_dir = "/tmp/github-runner-kadai/"


class TestConfigHandler(unittest.TestCase):
    def test_get_length(self):
        configHandler = ConfigHandler()
        configHandler.setConfigFilePath("tests/assets/non_config.json")
        self.assertEqual(len(configHandler.get()), 6)

        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

    def test_save(self):
        configHandler = ConfigHandler()
        configHandler.setConfigFilePath("tests/assets/non_config.json")
        configHandler.setConfigFileOutPath(os.path.join(out_dir, "config.json"))
        configHandler.save()

        self.assertTrue(os.path.isfile(os.path.join(out_dir, "config.json")))

        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

    def test_load(self):
        configHandler = ConfigHandler()
        configHandler.setConfigFilePath("tests/assets/non_config.json")
        configHandler.load("tests/assets/config.json")

        self.assertEqual(configHandler.get()["light_theme"], False)

    def test_compare_flag_with_config(self):
        configHandler = ConfigHandler()
        configHandler.setConfigFilePath("tests/assets/non_config.json")

        config = configHandler.get()
        self.assertTrue(config_handler.compareFlagWithConfig(True, config["light"]))
        self.assertFalse(config_handler.compareFlagWithConfig(False, config["light"]))
