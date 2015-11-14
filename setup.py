#!/usr/bin/env python

version = '0.1.2.dev0'

from distutils.core import setup

from codecs import open
from os import path

packages_list = ['cygenja',
                 'tests']

CLASSIFIERS = """\
Development Status :: 0 - Nowhere
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: Python
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Natural Language :: English
"""

here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name=  'cygenja',
      version=version,
      description='Cython code generator with Jinja2',
      long_description=long_description,
      #Author details
      author='Nikolaj van Omme, Sylvain Arreckx, Dominique Orban',

      author_email='nikolaj@funartech.com',

      maintainer = "Nikolaj van Omme",

      maintainer_email = "nikolaj@funartech.com",

      summary = "Cython code generator with Jinja2",
      url = "https://github.com/PythonOptimizers/cygenja",
      download_url = "https://github.com/PythonOptimizers/cygenja",
      license='LGPL',
      classifiers=filter(None, CLASSIFIERS.split('\n')),
      install_requires=['numpy', 'Cython'],
      #ext_package='cysparse', <- doesn't work with pxd files...
      #cmdclass = {'build_ext': build_ext},
      #ext_modules = ext_modules,
      package_dir = {"cygenja": "cygenja"},
      packages=packages_list,
      zip_safe=False
)