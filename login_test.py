# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.options import parse_config_file, options
from dojoapp import DojoApp

import dojo.auth
import mox

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

class LoginTest(AsyncHTTPTestCase):

    def setUp(self):
        self.mox = mox.Mox()
        super(LoginTest, self).setUp()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.ResetAll()
        super(LoginTest, self).tearDown()

    def get_app(self):
        return DojoApp(options)

    def test_access_login_and_be_redirect_to_twitter(self):
        self.mox.StubOutWithMock(dojo.auth.TwitterHandler, 'authorize_redirect', use_mock_anything=True)
        dojo.auth.TwitterHandler.authorize_redirect()
        self.mox.ReplayAll()
        response = self.fetch('/login/twitter')
        self.mox.VerifyAll()

    def test_access_login_with_callback(self):
        oauth = dict (
            oauth_token="31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4",
            oauth_verifier= "6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk",
        )
        self.mox.StubOutWithMock(dojo.auth.TwitterHandler, 'get_authenticated_user', use_mock_anything=True)
        self.mox.ReplayAll()
        args = urlencode(oauth)
        response = self.fetch('/login/twitter?'+args, follow_redirects=False)
        self.mox.VerifyAll()

    def test_access_login_with_callback(self):
        oauth = dict (
            oauth_token="31CYtN2gap7BL4t1m6o8oqQwz047VTg8rZXm9LHtOY4",
            oauth_verifier= "6bpcvonh0GWzZP4oUGyhq2BuMHt2cOe4kpuSYz7Rk",
        )
        self.mox.StubOutWithMock(dojo.auth.TwitterHandler, 'async_callback', use_mock_anything=True)
        self.mox.ReplayAll()
        args = urlencode(oauth)
        response = self.fetch('/login/twitter?'+args, follow_redirects=False)
        self.mox.VerifyAll()

if __name__ == '__main__':
    unittest.main()