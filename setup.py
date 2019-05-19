# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

from arrangeit import __version__


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='arrangeit',
    version=__version__,
    description='Cross-platform utility for easy placement of the visible windows on desktop',
    long_description=readme,
    packages=['arrangeit'],
    python_requires='~=3.5',
    install_requires=[
        'pynput',
        'pywin32; platform_system == "Windows"',
        'PyGObject; platform_system == "Linux"',
    ],
    author='Ivica Paleka',
    author_email='ipaleka@hopemeet.me',
    url='https://github.com/ipaleka/arrangeit',
    license=license,
)