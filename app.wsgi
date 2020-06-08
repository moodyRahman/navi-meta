#!/usr/bin/python3

import sys
sys.path.insert(0,'/var/www/{APPNAME}/')
sys.path.insert(0,'/var/www/{APPNAME}/{APPNAME}/')

import logging
logging.basicConfig(stream=sys.stderr)

from {APPNAME} import app as application
