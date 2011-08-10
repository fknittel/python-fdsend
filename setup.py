#!/usr/bin/env python

# fdsend setup.py

from setuptools import setup
from distutils.extension import Extension

setup(name = "fdsend",
      version = "0.1",
      description = "File descriptor passing (via SCM_RIGHTS)",
      author = "Michael J. Pomraning",
      author_email = "mjp-py@pilcrow.madison.wi.us",
      url = "http://pilcrow.madison.wi.us/fdsend",
      license = "GPL",
      packages = ['fdsend'],
      ext_modules = [Extension(name="_fdsend", sources=['_fdsend.c'])],
      test_suite = "fdsend.tests",
      )
