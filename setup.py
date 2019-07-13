# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import find_packages, setup

from arrangeit import __version__

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="arrangeit",
    version=__version__,
    description="Cross-platform desktop utility for easy windows management",
    long_description=readme,
    packages=find_packages(),
    python_requires="~=3.4",
    install_requires=[
        "Pillow",
        "pynput",
        'pyobjc-core; platform_system == "Darwin"',
        'pyobjc-framework-Cocoa; platform_system == "Darwin"',
        'pyobjc-framework-Quartz; platform_system == "Darwin"',
        'PyGObject; platform_system == "Linux"',
        'python-xlib; platform_system == "Linux"',
        'pywin32; platform_system == "Windows"',
    ],
    entry_points={"gui_scripts": ["arrangeit=arrangeit.__main__:main"]},
    author="Ivica Paleka",
    author_email="ipaleka@hopemeet.me",
    url="https://github.com/ipaleka/arrangeit",
    license=license,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
    ],
)
