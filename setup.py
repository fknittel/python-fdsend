#!/usr/bin/env python

from setuptools import setup
from distutils.extension import Extension

setup(
    name="fdsend",
    version="0.2.0pr1",
    description="File descriptor passing (via SCM_RIGHTS)",
    author="Michael J. Pomraning",
    author_email="mjp-py@pilcrow.madison.wi.us",
    maintainer="Philipp Kern and Fabian Knittel",
    maintainer_email="python-fdsend@googlegroups.com",
    url="https://gitorious.org/python-fdsend/pages/Home",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    packages=['fdsend'],
    ext_modules=[Extension(name="_fdsend", sources=['_fdsend.c'])],
    test_suite="fdsend.tests",
    long_description="""\
fdsend is yet another file descriptor passing abstraction, specifically for
Python.  This package offers a few conveniences not commonly found together in
other abstractions: sending multiple files at once, sending arbitrary data, and
working with both files and file descriptors.""",
    )
