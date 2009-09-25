#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import sys

if not (2, 4) < sys.version_info[:2] :
    raise Exception("backloglib requires a Python 2 version newer than 2.4. \n now running on %s" % sys.version)

setup(
      name = "backloglib",
      version = "0.1",
      author = "Takashi Someda",
      author_email = "someda@isenshi.com",
      url = "http://code.google.com/p/backloglib/",
      download_url = "http://code.google.com/p/backloglib/downloads/list",
      description = "Backlog client library",
      long_description ="",
      platforms = "any",      
      packages=['backloglib'],
      package_dir={"backloglib":"src/backloglib"},
      keywords = "backlog client",
      classifiers = [
                     "Operating System :: OS Independent",
                     "Environment :: Console",
                     "Programming Language :: Python",
                     "License :: OSI Approved :: Apache Software License",
                     "Development Status :: 2 - Pre-Alpha",
                     "Intended Audience :: Developers",
                     "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
                     "Topic :: Software Development :: Libraries :: Python Modules",
                     "Topic :: Utilities" 
                     ]
      )
