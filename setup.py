#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
from setuptools import setup
from setuptools import find_packages

from docs import get_version


CHANGELOG = open('CHANGES.rst').read()
LONG_DESCRIPTION = "\n\n".join([
    open('README.rst').read(),
    CHANGELOG
])


setup(
    name='rdiff_trimmer',
    version=get_version(CHANGELOG),
    py_modules=['rsync_trimmer'],

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    url='https://github.com/Bystroushaak/rdiff_trimmer',
    license='MIT',
    description='Get rid of the old rdiff-backup increments from your backup.',

    long_description=LONG_DESCRIPTION,

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,

    classifiers=[
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],

    scripts=[
        'bin/rdiff_trimmer',
        'bin/unpack_rdiff_increments',
    ],

    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    }
)
