#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='b2tob3',
    version='0.1',
    packages=find_packages(),
    long_description=README,
    license=LICENSE,
    author='Ramiro Gómez',
    author_email='code@ramiro.org',
    description='Help migrate HTML files and templates form bootstrap 2 to 3.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Text Processing',
    ],
    entry_points={
        'console_scripts': [
            'b2tob3= b2tob3.b2tob3:main'
        ]
    }
)