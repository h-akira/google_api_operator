#!/usr/bin/env python3
from setuptools import setup, find_packages

def requirements_from_file(file_name):
  return open(file_name).read().splitlines()

setup(name='google_api_operator',version='1.0.1',packages=find_packages(), install_requires=requirements_from_file('requirements.txt'))
