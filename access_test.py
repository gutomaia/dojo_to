# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.options import parse_config_file, parse_command_line, options
from dojoapp import DojoApp
from tornado import database

from testutils import init_db, drop_db

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

drop_db()
init_db()

class AccessTest(AsyncHTTPTestCase):

    def get_app(self):
        return DojoApp(options)

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEquals(200, response.code)
        self.assertNotRegexpMatches(response.body,r'None')

    def test_dojos(self):
        response = self.fetch('/dojos')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')
        self.assertNotRegexpMatches(response.body,r'None')


    def test_timeline(self):
        response = self.fetch('/timeline')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')
        self.assertNotRegexpMatches(response.body,r'None')

    def test_access_dojo_1_page(self):
        response = self.fetch('/dojo/1')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')

    def test_access_dojo_2_page(self):
        response = self.fetch('/dojo/2')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')

    def test_access_dojo_3_page(self):
        response = self.fetch('/dojo/3')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')

    def test_access_dojo_4_page(self):
        response = self.fetch('/dojo/4')
        self.assertEquals(404, response.code)

    def test_access_dojo_to_learn_python(self):
        response = self.fetch('/learn/python')
        self.assertEquals(200, response.code)
        self.assertRegexpMatches(response.body, r'<title>.+</title>')

    def test_access_dojo_to_learn_java(self):
        response = self.fetch('/learn/java')
        self.assertEquals(200, response.code)
        self.assertNotRegexpMatches(response.body,r'None')

    def test_access_dojo_to_learn_php(self):
        response = self.fetch('/learn/php')
        self.assertEquals(200, response.code)
        self.assertNotRegexpMatches(response.body,r'None')

    def test_access_dojo_to_learn_python_in_sao_paulo(self):
        response = self.fetch('/learn/python/in/sao_paulo')
        self.assertEquals(200, response.code)
        self.assertNotRegexpMatches(response.body,r'None')

if __name__ == '__main__':
    unittest.main()
