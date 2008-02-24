#!/usr/bin/python

from setuptools import setup, find_packages
import sys, os

version = '0.9'

setup(name='workerpool',
      version=version,
      description="Module for distribution jobs to a pool of worker threads.",
      long_description="""\
Super elegant, super expandable, super fun.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='pooling, threading, jobs',
      author='Andrey Petrov',
      author_email='andrey.petrov@shazow.net',
      url='http://code.google.com/p/workerpool/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
