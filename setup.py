

import os

from eveauth import __version__

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='eveauth',
    version=__version__,
    description=('A library for working with the EVE Online SSO.'),
    url='https://github.com/regner/eveauth',
    packages=find_packages(),
    long_description=read('README.md'),
)
