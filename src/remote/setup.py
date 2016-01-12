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
          'PyCrypto',
          'barrel',
          'fanstatic',
          'js.jquery',
          'wsgiproxy',
          'zope.interface',
          'repoze.who',
          'requests',
          'dolmen.template[cromlech]',
      ],
      tests_require=tests_require,
      extras_require={
            'test': tests_require
        },
      entry_points={
          'paste.composite_factory': [
              'remotehub = remote:hub_factory',
          ],
          'fanstatic.libraries': [
              'remote_wsgi = remote.resources:library',
          ],
          'paste.app_factory': [
              'proxy = remote:make_proxy',
          ],
          'paste.filter_app_factory': [
              'cipher = remote.ticket:cipher',
          ],
      },
      )
