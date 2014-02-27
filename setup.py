#!/usr/bin/env python
import contextlib
import os
import re
from setuptools import setup, find_packages
import shutil
import subprocess
import sys
import urllib2

README = os.path.join(os.path.dirname(__file__), 'README.txt')
long_description = open(README).read() + '\n\n'

PACKAGE = "petrel"

PETREL_VERSION = '0.1'


@contextlib.contextmanager
def chdir(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def get_storm_version():
    version = subprocess.check_output(['storm', 'version']).strip()
    m = re.search('^\d\.\d\.\d', version)
    return m.group(0)


def get_version(argv):
    """ Dynamically calculate the version based on VERSION."""
    return '%s.%s' % (get_storm_version(), PETREL_VERSION)


def build_petrel():
    version = get_storm_version()

    # Generate Thrift Python wrappers.
    if os.path.isdir('petrel/generated'):
        shutil.rmtree('petrel/generated')
    os.mkdir('petrel/generated')
    f_url = urllib2.urlopen(
        'https://raw.github.com/apache/incubator-storm/%s/src/storm.thrift' % version)

    with open('storm.thrift', 'w') as f:
        f.write(f_url.read())
    f_url.close()

    with chdir('petrel/generated'):
        subprocess.check_call(['thrift', '-gen', 'py', '-out', '.', '../../storm.thrift'])
    os.remove('storm.thrift')

    # Build JVMPetrel.
    with chdir('jvmpetrel'):
        subprocess.check_call(['mvn', '-Dstorm_version=%s' % version, 'assembly:assembly'])

    shutil.copyfile(
        'jvmpetrel/target/storm-petrel-%s-SNAPSHOT.jar' % version,
        'petrel/generated/storm-petrel-%s-SNAPSHOT.jar' % version)

if 'bdist_egg' in sys.argv or 'develop' in sys.argv:
    build_petrel()

setup(name=PACKAGE,
      version=get_version(sys.argv),
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
