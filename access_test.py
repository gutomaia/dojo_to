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


drop_db()
init_db()


class AccessTest(AsyncHTTPTestCase):

    def get_app(self):
        return DojoTo(options)

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEquals(200, response.code)
        #self.assertRegexpMatches(response.body,r'.*Hello.*')

    def test_access_dojo_to_learn_python(self):
        response = self.fetch('/learn/python')
        self.assertEquals(200, response.code)

    def test_access_dojo_to_learn_java(self):
        response = self.fetch('/learn/java')
        self.assertEquals(200, response.code)

    def test_access_dojo_to_learn_php(self):
        response = self.fetch('/learn/php')
        self.assertEquals(200, response.code)

    def test_access_dojo_to_learn_python_in_sao_paulo(self):
        response = self.fetch('/learn/python/in/sao_paulo')
        self.assertEquals(200, response.code)

if __name__ == '__main__':
    unittest.main()
