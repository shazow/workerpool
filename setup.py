#!/usr/bin/python

from setuptools import setup, find_packages
import sys, os

version = '0.9'

setup(name='workerpool',
      version=version,
      description="Module for distribution jobs to a pool of worker threads.",
      long_description="""\
Performing tasks in many threads made fun!

This module facilitates distributing simple operations into jobs that are sent to worker threads, maintained by a pool object.

It consists of these components:

   1. Jobs, which are single units of work that need to be performed.
   2. Workers, who grab jobs from a queue and perform them.
   3. Worker pool, which keeps track of workers and the job queue.
""",
      classifiers = [ # Strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Operating System :: MacOS :: MacOS X',
      'License :: OSI Approved :: MIT License',
      ],
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
