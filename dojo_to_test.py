# -*- coding: utf-8 -*-

import unittest, os, os.path, sys, urllib
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.options import parse_config_file, parse_command_line, options
from dojoapp import DojoApp
from tornado import database
from tornado.escape import json_encode, json_decode

from testutils import init_db, drop_db
import mox

from dojo.common import BaseHandler

from dojo.api import DojoApiHandler, ParticipantApiHandler

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(APP_ROOT, '.'))

parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        super(BaseTest, self).setUp()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.ResetAll()
        super(BaseTest, self).tearDown()

    def test_get_current_user_with_a_user_logged(self):
        self.mox.StubOutWithMock(BaseHandler, 'get_cookie', use_mock_anything=True)
        self.mox.StubOutWithMock(BaseHandler, 'get_secure_cookie', use_mock_anything=True)
        BaseHandler.get_cookie('user').AndReturn('lot of stuff')
        BaseHandler.get_secure_cookie('user').AndReturn('ok')
        self.mox.ReplayAll()
        #base = BaseHandler(None,None)
        #base.get_current_user();
        




class DojoToTest(unittest.TestCase):

    def test_twitter_handler_on_auth(self):
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
        super(DojoToHttpTest, self).tearDown()

    def get_app(self):
        app = DojoApp(options)
        self.mox.StubOutWithMock(DojoApiHandler, 'get_current_user', use_mock_anything=True)
        self.logged_user = dict(
            id = 1,
            twitter_id = 13818022,
            username = 'gutomaia',
            url = 'http://gutomaia.com',
            twitter_display_icon = 'http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg'
        )
        return app

    def test_create_a_dojo_with_a_simple_post(self):
        '''
        Create a dojo using a simple post, this api will be used
        on forms from the page, when the user hasn't javascript enabled.

        TODO: date_hour must be passed somehow!?
        TODO: if they are separated fields?!? The server code must catch
        with GMT user is and make the correct conversion!

        How to render it to a microformat?!

        '''
        DojoApiHandler.get_current_user().AndReturn(self.logged_user)
        DojoApiHandler.get_current_user().AndReturn(self.logged_user)
        self.mox.ReplayAll()
        expected = dict(
            language = "python",
            location = 'GruPy HeadQuarters',
            address = 'Rua A Ser definida mas com varios caracteres, 42, Bairro',
            city = 'São Paulo',
            date_hour = 'Sex Out 21 18:40:23 BRST 2011'
        )
        body = urlencode(expected)
        headers = {'Accept': 'application/x-www-form-urlencoded'}
        response = self.fetch('/api/dojo', method='POST', body=body, follow_redirects=False, headers=headers)
        self.assertEquals(302, response.code)
        db = database.Connection("localhost", "dojo_to")
        dojos = db.execute_rowcount("SELECT * FROM dojos")
        self.assertEquals(4, dojos)
        actual = db.get('SELECT * from dojos WHERE id = 4')
        self.assertEquals(expected['language'], actual['language'])
        self.assertEquals(expected['location'], actual['location'])
        self.assertEquals(expected['address'], actual['address'])
        self.assertEquals(expected['city'], actual['city'])
        db.close()
        self.mox.VerifyAll()


    
    def test_timestamp_conversion(self):
        '''
        Av. Brigadeiro Faria Lima nº 3900 5th floor, Itaim Sao Paulo
        If user is in GMT -3 and at 21hrs from january 1 he set sometihng,
        then the record on the database must be at 00:00 on january 2.
        '''
        pass
    
    def test_timestamp_format(self):
        '''
        If a timestamp catched from the database on a specific hour
        on a GMT-0
        must be formated as 2011-10-27T19:00-02:0000
        on GMT-2
        '''
        pass
        
    def test_create_a_dojo_from_a_json(self):
        DojoApiHandler.get_current_user().AndReturn(self.logged_user)
        DojoApiHandler.get_current_user().AndReturn(self.logged_user)
        self.mox.ReplayAll()
        expected = dict(
            language = "python",
            location = 'GruPy HeadQuarters',
            address = 'asdf',
            city = 'São Paulo',
            date_hour = 'Sex Out 21 18:40:23 BRST 2011'
        )
        headers = {'Accept': 'application/json'}
        body = json_encode(expected)
        response = self.fetch('/api/dojo', method='POST', body=body, follow_redirects=False, headers=headers)
        self.assertEquals(200, response.code)
        db = database.Connection("localhost", "dojo_to")
        dojos = db.execute_rowcount("SELECT * FROM dojos")
        self.assertEquals(4, dojos)
        actual = db.get('SELECT * from dojos WHERE id = 4')
        self.assertEquals(expected['language'], actual['language'])
        self.assertEquals(expected['location'], actual['location'])
        self.assertEquals(expected['address'], actual['address'])
        self.assertEquals(expected['city'], actual['city'])
        db.close()
        self.mox.VerifyAll()


class ParticipantApiTest(AsyncHTTPTestCase):

    def setUp(self):
        self.mox = mox.Mox()
        drop_db()
        init_db()
        super(ParticipantApiTest, self).setUp()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.ResetAll()
        super(ParticipantApiTest, self).tearDown()

    def get_app(self):
        app = DojoApp(options)
        self.mox.StubOutWithMock(ParticipantApiHandler, 'get_current_user', use_mock_anything=True)
        self.logged_user = dict(
            id = 1,
            twitter_id = 13818022,
            username = 'gutomaia',
            url = 'http://gutomaia.com',
            twitter_display_icon = 'http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg'
        )
        return app

    def test_join_dojo_2_with_a_simple_post(self):
        ParticipantApiHandler.get_current_user().AndReturn(self.logged_user)
        ParticipantApiHandler.get_current_user().AndReturn(self.logged_user)
        self.mox.ReplayAll()
        expected = dict(
            dojo_id = 2
        )

        body = urlencode(expected)
        headers = {'Accept': 'application/x-www-form-urlencoded'}

        db = database.Connection("localhost", "dojo_to")
        join = db.get("SELECT * FROM participants WHERE user_id=1 AND dojo_id=2")
        self.assertIsNone(join)

        response = self.fetch('/dojo/2/join', method='POST', body=body,
            follow_redirects=False, headers=headers
        )
        self.assertEquals(302, response.code)
        participants = db.execute_rowcount("SELECT * FROM participants")
        self.assertEquals(4, participants)
        join = db.get("SELECT * FROM participants WHERE user_id=1 AND dojo_id=2")
        self.assertIsNotNone(join)
        self.assertEquals(1, join.user_id)
        self.assertEquals(2, join.dojo_id)
        self.assertFalse(join.confirmed) #TODO

        db.close()
        self.mox.VerifyAll()

    def test_join_dojo_2_witch_i_m_already_in(self):
        ParticipantApiHandler.get_current_user().AndReturn(self.logged_user)
        ParticipantApiHandler.get_current_user().AndReturn(self.logged_user)
        self.mox.ReplayAll()

        db = database.Connection("localhost", "dojo_to")

        #query = "INSERT INTO participants (user_id, dojo_id) VALUES (1,2)"
        #db.query(query)

        expected = dict(
            dojo_id = 2
        )

        body = urlencode(expected)
        headers = {'Accept': 'application/x-www-form-urlencoded'}

        #TODO
        #response = self.fetch('/dojo/2/join', method='POST', body=body,
        #    follow_redirects=False, headers=headers
        #)
        #self.assertEquals(302, response.code)
        db.close()
        #self.mox.VerifyAll()

if __name__ == '__main__':
    unittest.main()