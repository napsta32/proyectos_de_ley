# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '2.1.1'

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
        'Django==1.8.4',
    ],
    zip_safe=False,
    scripts=['proyectos_de_ley/manage.py'],
)
