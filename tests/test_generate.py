import unittest
import shutil
import os
from kadai.utils import FileUtils
from kadai import themer
from kadai.engine import HueEngine
from kadai.config_handler import ConfigHandler

out_dir = "/tmp/github-runner-kadai/"
assets_dir = "tests/assets/"
config_path = os.path.join(assets_dir, "config.json")

configHandler = ConfigHandler()
configHandler.setConfigFilePath(config_path)
config = configHandler.get()


class TestEngines(unittest.TestCase):
    def test_template_find(self):
        # Test if can find all 2 template files
        template_files = themer.get_template_files(
            os.path.join(assets_dir, "templates/")
        )
        self.assertEqual(len(template_files), 2)

    def test_createValueSpreadDictionary(self):
        values = [0.1, 0.3, 0.5, 0.7, 0.9]
        pallete = themer.createValueSpreadDictionary(values, (255, 0, 0))
        self.assertEqual(
            pallete,
            {
                "0.1": "#190000",
                "0.3": "#4c0000",
                "0.5": "#7f0000",
                "0.7": "#b20000",
                "0.9": "#e50000",
            },
        )

    def test_createValueColorPallete(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        pallete = themer.createValueColorPallete(colors)
        self.assertEqual(
            pallete,
            {
                "color0": {
                    "0.1": "#190000",
                    "0.3": "#4c0000",
                    "0.5": "#7f0000",
                    "0.7": "#b20000",
                    "0.9": "#e50000",
                },
                "color1": {
                    "0.1": "#001900",
                    "0.3": "#004c00",
                    "0.5": "#007f00",
                    "0.7": "#00b200",
                    "0.9": "#00e500",
                },
                "color2": {
                    "0.1": "#000019",
                    "0.3": "#00004c",
                    "0.5": "#00007f",
                    "0.7": "#0000b2",
                    "0.9": "#0000e5",
                },
            },
        )

    def test_generate_one(self):
        # Testing for generating one theme
        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

        generator = themer.Themer("tests/assets/test.jpg", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.generate()

        self.assertIs(
            os.path.isfile(
                os.path.join(out_dir, "themes/31084f2c8577234aeb55-vibrance.json")
            ),
            True,
        )

    def test_generate_all(self):
        # Testing for generating all images into themes
        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")

        generator = themer.Themer("tests/assets/", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.generate()

        self.assertTrue(
            os.path.isfile(
                os.path.join(out_dir, "themes/31084f2c8577234aeb55-vibrance.json")
            )
        )

    def test_update(self):
        # Test if update passes when theme file exists
        generator = themer.Themer("tests/assets/test.jpg", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.setRunHooks(True)
        generator.setUserTemplatePath(os.path.join(assets_dir, "templates/"))
        generator.setUserHooksPath(os.path.join(assets_dir, "hooks/"))
        generator.update()

        self.assertTrue(os.path.isfile(os.path.join(out_dir, "colors.sh")))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "Xdefaults")))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "out")))

    def test_update_no_templates(self):
        generator = themer.Themer("tests/assets/test.jpg", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.setRunHooks(True)
        generator.setUserTemplatePath(out_dir)
        generator.update()

    def test_update_light_theme(self):
        # Test if update passes when theme file exists
        generator = themer.Themer("tests/assets/test.jpg", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.setRunHooks(False)
        generator.setUserTemplatePath(os.path.join(assets_dir, "templates/"))
        generator.enableLightTheme()
        generator.update()

        self.assertTrue(os.path.isfile(os.path.join(out_dir, "colors.sh")))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "Xdefaults")))

    def test_update_folder(self):
        generator = themer.Themer(assets_dir, out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.setRunHooks(False)
        generator.setUserTemplatePath(os.path.join(assets_dir, "templates/"))
        generator.generate()
        generator.update()

        self.assertTrue(os.path.isfile(os.path.join(out_dir, "colors.sh")))
        self.assertTrue(os.path.isfile(os.path.join(out_dir, "Xdefaults")))

    def test_update_file_not_recognised(self):
        generator = themer.Themer("tests/assets/test.txt", out_dir, config=config)
        generator.setRunHooks(False)
        try:
            generator.update()
            raise ValueError("How!?")
        except FileUtils.noPreGenThemeError:
            pass

    def test_update_not_find_generated(self):
        # Test if fail if theme file does not exist
        generator = themer.Themer("tests/assets/test.jpg", out_dir, config=config)
        generator.setCachePath(out_dir)
        generator.setRunHooks(False)
        shutil.rmtree(out_dir, ignore_errors="FileNotFoundError")
        try:
            generator.update()
            raise ValueError("Passed Succesfully?!")
        except FileUtils.noPreGenThemeError:
            pass

    def test_class_options(self):
        generator = themer.Themer("tests/assets/test.png", "tmp", config=config)

        generator.setImagePath("tests/assets/test.jpg")
        self.assertEqual(generator.image_path, "tests/assets/test.jpg")

        generator.setOutPath(out_dir)
        self.assertEqual(generator.out_path, out_dir)

        generator.setEngine("hue")
        self.assertEqual(generator.engine_name, "hue")
        self.assertEqual(generator.engine, HueEngine)

        generator.setOverride(True)
        self.assertEqual(generator.override, True)

        generator.setUserTemplatePath("/tmp/templates")
        self.assertEqual(generator.user_templates_path, "/tmp/templates")

        generator.setRunHooks(False)
        self.assertEqual(generator.run_hooks, False)

        generator.disableProgress(False)
        self.assertEqual(generator.disable_progress, False)

        generator.enableLightTheme()
        self.assertEqual(generator.light_theme, True)


if __name__ == "__main__":
    unittest.main()
