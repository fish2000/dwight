#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2012 Alexander Böhn
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
dwight
======

Run Django management commands against arbitrary settings files.

Copyright © 2012 Alexander Böhn.
This software is licensed under the terms of the GNU General Public
License version 2 as published by the Free Software Foundation.

"""

import os, os.path
name = 'dwight'
version = '0.8.0'
packages = []
package_data = {}
description = 'Run Django management commands against arbitrary settings files.'
keywords = 'django management command execute run settings'

classifiers = [
    'Development Status :: 5 - Production/Stable']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import shutil
if not os.path.exists('src/scripts'):
    os.makedirs('src/scripts')
shutil.copyfile('src/dwight/dwight.py', 'src/scripts/dwight')
os.chmod('src/scripts/dwight', 0755)

setup(
    name=name, version=version, description=description,
    download_url = 'http://github.com/fish2000/%s/zipball/master' % name,

    author=u"Alexander Böhn",
    author_email='fish2000@gmail.com',
    url='http://github.com/fish2000/%s/' % name,
    license='GPLv2',
    
    keywords=keywords,
    platforms=['any'],
    packages=['dwight'],
    package_dir={'dwight': 'src/dwight'},
    package_data=package_data,
    scripts={ 'src/scripts/dwight': 'dwight'},
    
    install_requires=[
    'userconfig',
    'argparse',
    'argh',
    'django>=1.3'],
    
    #entry_points={
    #    'console_scripts': [
    #        'dwight = dwight.dwight:main']},
    
    classifiers=classifiers+[
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.6'],
)
