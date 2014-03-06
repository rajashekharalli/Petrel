#!/usr/bin/env python
import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'README.txt')
long_description = open(README).read() + '\n\n'

PACKAGE = "petrel"

PETREL_VERSION = '0.1'

setup(name=PACKAGE,
      version='0.9.0.0.1',
      description=("Storm Topology Builder"),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          "Operating System :: POSIX :: Linux",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: System :: Distributed Computing",
      ],
      keywords='Storm Topology Builder',
      author='bhart',
      url='https://github.com/AirSage/Petrel',
      packages=find_packages(),
      package_data={'': ['*.jar']},
      license='BSD 3-clause',
      entry_points={
          'console_scripts': [
              'petrel = petrel.cmdline:main',
          ],
      },
      install_requires=[
          'simplejson==2.6.1',
          # Request specific Thrift version. Storm is in Java and may be
          # sensitive to version incompatibilities.
          'thrift==0.8.0',
          'PyYAML==3.10',
      ],
      # Setting this flag makes Petrel easier to debug within a running
      # topology.
      zip_safe=False)
