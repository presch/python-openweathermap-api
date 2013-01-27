#!/usr/bin/env python

from distutils.core import setup

__version__ = '0.0.1'

setup(name='pyowm',
      version=__version__,
      description='A python wrapper around the Open Weather map api',
      author='Philipp Resch',
      url='https://github.com/presch/python-openweathermap-api',
      py_modules=['pyowm'],
      license='GPLv3',
      keywords = 'weather open weather map'
      )
