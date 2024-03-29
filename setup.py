from setuptools import setup

LONG_DESC = open("README.md").read()

setup(
    name="kadai",
    version="1.2.0a0",
    description="Simple wallpaper manager for tiling window managers.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
    url="http://github.com/slapelachie/kadai",
    author="slapelachie",
    author_email="slapelachie@gmail.com",
    license="GPLv2",
    packages=["kadai", "kadai.engine", "kadai.utils"],
    entry_points={"console_scripts": ["kadai=kadai.__main__:main"]},
    include_package_data=True,
    install_requires=["Pillow>=9.1.0", "tqdm", "colorthief"],
    zip_safe=False,
)
