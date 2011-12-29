#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
        name='ado',
        author='Ana Nelson',
        install_requires = [
            'python-modargs>=1.2'
            ],
        entry_points = {
            'console_scripts' : [ 'ado = ado.commands:run' ]
            }
        )

