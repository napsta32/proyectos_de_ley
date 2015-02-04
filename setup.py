# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import proyectos_de_ley
version = '1.7.0'

setup(
    name='proyectos_de_ley',
    version=version,
    author='Aniversario Peru',
    author_email='aniversarioperu1@gmail.com',
    packages=[
        'proyectos_de_ley',
    ],
    include_package_data=True,
    install_requires=[
        'Django==1.7.3',
    ],
    zip_safe=False,
    scripts=['proyectos_de_ley/manage.py'],
)
