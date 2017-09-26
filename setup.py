#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
	readme = readme_file.read()

setup(
	name='jarvis',
	version='1.0',
	url='https://github.com/imdahoe/jarvis',
	license='Apache Software License',
	long_description=readme,
	author='Simon Ho',
	author_email='simon.ho@mail.mcgill.ca',
	description='Just A Rather Very Intelligent System',
	packages=['jarvis'],
	platforms='any'
)