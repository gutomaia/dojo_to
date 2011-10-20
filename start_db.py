# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from testutils import init_db, drop_db

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

init_db()