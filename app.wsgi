#!/usr/bin/python3

import sys
sys.path.insert(0,'/var/www/navi-meta/')
sys.path.insert(0,'/var/www/navi-meta/navi-meta/')

import logging
logging.basicConfig(stream=sys.stderr)

from navi-meta import app as application
