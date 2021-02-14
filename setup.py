#!/usr/bin/env python
'''
Setup script for Mopidy-Pummeluff module.
'''



from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

with open('requirements_dev.txt') as f:
    requirements_dev = f.read().strip().split('\n')

setup(
    name='Mopidy-Pummeluff',
    use_scm_version=True,
    url='https://github.com/confirm/mopidy-pummeluff',
    license='MIT',
    author='confirm IT solutions',
    description='Pummeluff is a Mopidy extension which allows you to control Mopidy via RFID tags',
    long_description=open('README.rst').read()
)
