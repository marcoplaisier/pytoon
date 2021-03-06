#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pytoon',
    version='0.0.1',
    description='PyToon measures electricity, water and gas meters and creates fancy graphs',
    long_description=readme + '\n\n' + history,
    author='Marco Plaisier',
    author_email='m.plaisier@gmail.com',
    url='https://github.com/marcofinalist/pytoon',
    packages=[
        'pytoon',
    ],
    package_dir={'pytoon': 'pytoon'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='pytoon',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)