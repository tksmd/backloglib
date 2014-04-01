#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 - 2014 Takashi SOMEDA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from distutils.core import setup
import sys

if not (2, 5) <= sys.version_info[:2]:
    raise Exception("backloglib requires a Python 2 version newer than 2.5. \n now running on %s" % sys.version)

setup(
    name="backloglib",
    version="0.2.4",
    author="Takashi Someda",
    author_email="someda@isenshi.com",
    url="https://github.com/tksmd/backloglib/",
    download_url="https://github.com/tksmd/backloglib/archive/REL-0.2.4.tar.gz",
    description="Backlog client library",
    long_description="",
    platforms="any",
    packages=['backloglib'],
    package_dir={"backloglib": "src/backloglib"},
    keywords="backlog client",
    classifiers=[
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
