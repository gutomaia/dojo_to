# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.options import parse_config_file, parse_command_line, options
from dojo_to import DojoTo, TwitterHandler
from tornado import database

from testutils import init_db, drop_db

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/dojo_to.conf")

class LoginTest(AsyncHTTPTestCase):

    def setUp(self):
        drop_db()
        init_db()
        super(LoginTest, self).setUp()

    def get_app(self):
        return DojoTo(options)

    def test_access_login_and_be_redirect_to_twitter(self):
        #response = self.fetch('/login/twitter', follow_redirects=False)
        #assertEquals(301, response.code)
        pass

    def test_access_login_with_callback(self):
        oauth = dict (
            oauth_token="31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4",
            oauth_verifier= "6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk",
        )
        args = urlencode(oauth)
        #response = self.fetch('/login/twitter?'+args, follow_redirects=False)
        #token cookie
        #self.assertFalse(True)
        pass
        #oauth_token=31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4&oauth_verifier=6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk

if __name__ == '__main__':
    unittest.main()
