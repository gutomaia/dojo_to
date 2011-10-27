# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.options import parse_config_file, parse_command_line, options
from dojo_to import DojoTo
from tornado import database

from testutils import init_db, drop_db

from mock import patch

import dojo.auth

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

class LoginTest(AsyncHTTPTestCase):

    def setUp(self):
        drop_db()
        init_db()
        super(LoginTest, self).setUp()

    def get_app(self):
        dojo_to = DojoTo(options)
        for h in dojo_to.handlers:
            print h[1][0].handler_class
        #print dojo_to.handlers
        return dojo_to

    def test_access_login_and_be_redirect_to_twitter(self):
        #response = self.fetch('/login/twitter', follow_redirects=False)
        #assertEquals(301, response.code)
        pass

    def test_access_login_with_callback(self):
        oauth = dict (
            oauth_token="31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4",
            oauth_verifier= "6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk",
        )
        #application = [];
        #TwitterHandler(application=None, request=None)
        #patcher = patch('TwitterHandler')
        #mocked = patcher.start()
        #self.get_authenticated_user(self.async_callback(self._on_auth))
        #patcher.stop()
        args = urlencode(oauth)

        #handler = self.
        #response = self.fetch('/login/twitter?'+args, follow_redirects=False)
        #self.assertEquals(302, response.code)

        #token cookie
        #self.assertFalse(True)
        #oauth_token=31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4&oauth_verifier=6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk

if __name__ == '__main__':
    unittest.main()
