# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.options import parse_config_file, parse_command_line, options
from dojo_to import DojoTo, TwitterHandler
from tornado import database
from tornado.escape import json_encode, json_decode

from testutils import init_db, drop_db
import mox

from dojo_to import DojoApiHandler

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

class DojoToTest(unittest.TestCase):

    def test_twitter_handler_on_auth(self):
 #       th = TwitterHandler();
        self.assertTrue(True)

class DojoToHttpTest(AsyncHTTPTestCase):

    def setUp(self):
        self.mox = mox.Mox()
        drop_db()
        init_db()
        super(DojoToHttpTest, self).setUp()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.ResetAll()
        #super(DojoToHttpTest, self).tearDown()

    def get_app(self):
        #self.mox.CreateMock(DojoTo)
        app = DojoTo(options)
        self.mox.StubOutWithMock(DojoApiHandler, 'get_current_user', use_mock_anything=True)
        logged_user = dict(
            id = 1,
            twitter_id = 21313,
            username = 'gutomaia',
            url = 'http://',
            twitter_display_icon = 'asdf'
        )
        DojoApiHandler.get_current_user().AndReturn(logged_user)
        return app

    def test_create_a_dojo_with_a_simple_post(self):
        self.mox.ReplayAll()
        form = dict(
            language = "python",
            location = 'GruPy HeadQuarters',
            address = 'asdf',
            city = 'São Paulo',
            date_hour = 'Sex Out 21 18:40:23 BRST 2011'
        )
        body = urlencode(form)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.fetch('/api/dojo', method='POST', body=body, follow_redirects=False)
        self.assertEquals(302, response.code)
        db = database.Connection("localhost", "dojo_to")
        dojos = db.execute_rowcount("SELECT * FROM dojos")
        self.assertEquals(4, dojos)
        db.close()
        self.mox.VerifyAll()
        
    def test_create_a_dojo_from_a_json(self):
        self.mox.ReplayAll()
        form = dict(
            language = "python",
            location = 'GruPy HeadQuarters',
            address = 'asdf',
            city = 'São Paulo',
            date_hour = 'Sex Out 21 18:40:23 BRST 2011'
        )
        headers = {'Content-Type': 'application/json'}
        body = json_encode(form)
        response = self.fetch('/api/dojo', method='POST', body=body, follow_redirects=False, headers=headers)
        self.assertEquals(200, response.code)
        db = database.Connection("localhost", "dojo_to")
        dojos = db.execute_rowcount("SELECT * FROM dojos")
        self.assertEquals(4, dojos)
        self.mox.VerifyAll()

if __name__ == '__main__':
    unittest.main()
