# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from tornado.testing import AsyncHTTPTestCase, main
from tornado.web import Application
from tornado.options import parse_config_file, parse_command_line, options
from dojo_to import DojoTo
import tornado.database

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(os.path.join(APP_ROOT, '.'))

def clear_db(app=None):
    #os.system("mysql %s < %s" % (options.mysql_database, os.path.join(APP_ROOT, 'db', 'schema.sql')))
    pass

class DojoToTest(AsyncHTTPTestCase):

    def setUp(self):
        clear_db()
        super(DojoToTest, self).setUp()

    def get_app(self):
        parse_config_file("/Users/gutomaia/dojo_to.conf")
        return DojoTo(options)

    def test_db(self):
        db = database.Connection("localhost", "dojo_to")
        for users in db.query("SELECT * FROM users"):
            print users.title


    def test_homepage(self):
        #self.http_client.fetch(self.get_url('/'), self.stop)
        #response = self.wait()
        response = self.fetch('/')
        self.assertEquals(200, response.code)
        #self.assertRegexpMatches(response.body,r'.*Hello.*')

    '''        
    def test_userpage(self):
        response = self.fetch('/guto')
        self.assertEquals(200, response.code)

    def test_template(self):
        response = self.fetch('/template')
        self.assertEquals(200, response.code)

    def test_template2(self):
        response = self.fetch('/template2')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body,r'.*<title>.*</title>.*')

    def test_json(self):
        response = self.fetch('/json')
        self.assertEquals(200, response.code)
        self.assertTrue(response.headers['Content-Type'] == 'application/json', "Content-Type is not a application/json")

    def test_login(self):
        #response = self.fetch('/login', follow_redirects=False)
        #response = self.fetch('/login')
        #self.assertEquals(302, response.code)
        #self.assertTrue(response.headers['Location'].endswith('/tutorial'), "response.headers[Location'] did not ends with /tutorial")
        pass
    '''

if __name__ == '__main__':
    unittest.main()