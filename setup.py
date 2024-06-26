#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: David Versmisse <david.versmisse@itaapy.com>
#          Hervé Cauwelier <herve@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.net).
# Lpod is free software; you can redistribute it and/or modify it under
# the terms of either:
#
# a) the GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    Lpod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with Lpod.  If not, see <http://www.gnu.org/licenses/>.
#
# b) the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#

from setuptools import setup
import os
from sys import executable
import re

# Import local
from release import has_git, get_release

g = {}
exec(compile(open(os.path.join('lpod', '_version.py'), "rb").read(), os.path.join('lpod', '_version.py'), 'exec'), g)
lpod_version = g['__version__']

#if has_git():
#    release = '-'.join((lpod_version, get_release()))
#else:
release = lpod_version

# Find all the scripts => It's easy: all the files in scripts/
scripts = [ os.path.join('scripts', filename)
           for filename in os.listdir('scripts') ]

# Make the python_path.txt file
open('python_path.txt', 'w').write(executable)

setup(description='lpOD Library',
      license='GPLv3 + Apache v2',
      name='lpod-python3',
      package_data={'': ['templates/*']},
      package_dir={'lpod': 'lpod'},
      scripts=scripts,
      packages=['lpod'],
      url='http://www.lpod-project.net/',
      version=release,
      author="lpOD Team",
      author_email="team@lpod-project.net")
