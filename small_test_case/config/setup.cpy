#!/usr/bin/env python
# The file setup.py is automatically generated
# Generate it with
# python generate_code

from distutils.core import setup
from setuptools import find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np

import ConfigParser
import os
import copy

from codecs import open
from os import path

config = ConfigParser.SafeConfigParser()
config.read('site.cfg')

version = {}
with open(os.path.join('small_test_case', 'version.py')) as fp:
      exec(fp.read(), version)
# later on we use: version['version']

numpy_include = np.get_include()


# EXTENSIONS
# ==========
include_dirs = [numpy_include, '.']

ext_params = {}
ext_params['include_dirs'] = include_dirs
ext_params['extra_compile_args'] = ["-O2", '-std=c99', '-Wno-unused-function']
ext_params['extra_link_args'] = []

ext = []
{% for index_type in index_list %}
  {% for element_type in type_list %}
ext_params_@index_type@_@element_type@ = copy.deepcopy(ext_params)
ext.append(Extension(name="small_test_case.src.basic_@index_type@_@element_type@",
                     sources=['small_test_case/src/basic_@index_type@_@element_type@.pxd',
                              'small_test_case/src/basic_@index_type@_@element_type@.pyx'],
                     **ext_params_@index_type@_@element_type@))
  {% endfor %}
{% endfor %}

packages_list = ['small_test_case', 'small_test_case.src']

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: Python
Programming Language :: Cython
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Natural Language :: English
"""

setup(name='small_test_case',
      version=version['version'],
      description='A small test case using cygenja',
      #Author details
      author='Sylvain Arreckx, Dominique Orban and Nikolaj van Omme',
{% raw %}
      author_email='sylvain.arreckx@gmail.com',
{% endraw %}
      maintainer = "Sylvain Arreckx",
{% raw %}
      maintainer_email = "sylvain.arreckx@gmail.com",
{% endraw %}
      summary = "A small test case using cygenja",
      url = "...",
      download_url = "...",
      license='LGPL',
      classifiers=filter(None, CLASSIFIERS.split('\n')),
      install_requires=['numpy', 'Cython'],
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext,
      package_dir = {"small_test_case": "small_test_case"},
      packages=packages_list,
      zip_safe=False
)
