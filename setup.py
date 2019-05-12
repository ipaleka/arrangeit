# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='arrangeit',
    version='0.0.1',
    description='Cross-platform utility for easy placement of the visible windows on desktop',
    long_description=readme,
    author='Ivica Paleka',
    author_email='ipaleka@hopemeet.me',
    url='https://github.com/ipaleka/arrangeit',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)