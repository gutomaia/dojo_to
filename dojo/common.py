# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth
from tornado import database
from tornado.escape import json_decode

class BaseHandler(tornado.web.RequestHandler):

    def get_database(self):
        db = database.Connection(
            self.settings['database_host'],
            self.settings['database_name'],
            self.settings['database_username'],
            self.settings['database_password']
        )
        return db

    def get_current_user(self):
        if self.get_cookie('user'): #TODO check for a non-secure-cookie
            return json_decode(self.get_secure_cookie('user'))
        return None

    def json_content(self):
        self.set_header('Content-Type', 'application/json')

    def get_accept_types(self):
        accept = self.request.headers.get('Accept')
        if accept:
            return self.request.headers['Accept'].split(',')
        else:
            return ['text/html']
