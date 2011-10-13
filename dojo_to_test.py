# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from subprocess import call
from urllib import urlencode


from tornado.testing import AsyncHTTPTestCase, main
from tornado.web import Application
from tornado.options import parse_config_file, parse_command_line, options
from dojo_to import DojoTo
from tornado import database

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/dojo_to.conf")


def mysql_run(file):
    try:
        retcode = call("mysql %s < %s" % ("dojo_to", os.path.join(APP_ROOT, 'sql', file)), shell=True)
        if retcode != 0:
            print >>sys.stderr, "Child was terminated by signal a", -retcode
            raise Exception("Mysql problem on: "+file)
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

def init_db(app=None):
    mysql_run('create_schema.sql')
    mysql_run('test_data.sql')

def drop_db(app=None):
    mysql_run('drop_schema.sql')


class DojoToTest(AsyncHTTPTestCase):

    def setUp(self):
        drop_db()
        init_db()
        super(DojoToTest, self).setUp()

    def get_app(self):
        return DojoTo(options)

    def test_db(self):
        db = database.Connection("localhost", "dojo_to")
        users = db.execute_rowcount("SELECT * FROM users")
        self.assertEquals(1, users);
        dojos = db.execute_rowcount("SELECT * FROM dojos")
        self.assertEquals(1, dojos);

        #for users in db.query("SELECT * FROM users"):
        #    print users.username
        #db.execute("INSERT INTO users (username) values(%s)", "guto maia")
        #self.assertTrue(False)

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEquals(200, response.code)
        #self.assertRegexpMatches(response.body,r'.*Hello.*')

    def test_form(self):
        form = dict(
            local = "gUTO.nET HeadQuarers",            
        )
        body = urlencode(form)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                

        pass

    def test_onlogin(self):
        pass

    def test_create_a_new_dojo(self):

        pass

    def test_on_user_enlist(self):

        pass
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
