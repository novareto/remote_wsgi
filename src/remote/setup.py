# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys, os

version = '0.0'

tests_require = [
    ]

setup(name='remote',
      version=version,
      description="",
      long_description=""" """,
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'barrel',
        'wsgiproxy',
      ],
      tests_require=tests_require,
      extras_require={
            'test': tests_require
        },
      entry_points={
         'paste.app_factory': [
             'proxy = remote:make_proxy',
         ],
      },
      )
