# -*- coding: utf-8 -*-

import os, os.path, sys, urllib

import tornado.ioloop
import tornado.web
import tornado.auth

from tornado.template import Template
from tornado.escape import json_encode, json_decode
from tornado.options import define, options

from tornado import httpclient
from tornado import database

from tornado.options import define, options

import logging

import dojo.api
import dojo.site
import dojo.auth

from dojo.common import BaseHandler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('dojolog')

define("port", help="Application Port", default=8888)

define("cookie_secret", help="App Cookie Secret")

define("debug", help="App Debug", default=False)

define("database_host", help="Database host", default="localhost")
define("database_port", help="Database port", default=3306)
define("database_name", help="Database name", default="dojo_to")
define("database_username", help="Database username", default=None)
define("database_password", help="Database password", default=None)

define("twitter_consumer_key", help="your Twitter application API key")
define("twitter_consumer_secret", help="your Twitter application secret")
define("twitter_callback", help="your twitter callback", default=None)

define("github_client_id", help="your Github application client id")
define("github_secret", help="your Github application secret")

class CrudDojoHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, id = None):
        if (id):
            pass
        self.render('dojo_form.html', dojo=dojo, logged_user = self.current_user)


class SocialApiHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, url):
        if url == 'friends':
            #if user has twitter
            self.twitter_request("/followers/ids", 
                access_token= user["access_token"],
                callback= self.async_callback(self._on_twitter_friends))
            #if user has facebook
        if url == 'comments':
            #self.twitter.r search twitter by dojo_id
            pass
        
        self.write('ok')
        
    def _on_twitter_friends(self): 
        query = "select username, twitter_display_icon  from users where twitter_id in (2,3) order by username"
        pass

    def _on_comments(self):
        pass

class DojoApp(tornado.web.Application):
    def __init__(self, options):
        handlers = [
            (r"/", dojo.site.Home),
            (r"/timeline", dojo.site.Timeline),
            (r"/learn/([A-Za-z_]+)", dojo.site.Dojo),
            (r"/learn/([A-Za-z_]+)/in/([A-Za-z_]+)", dojo.site.Dojo),

            (r"/dojo/([0-9]+)", dojo.api.DojoApiHandler),
            (r"/dojo/([0-9]+)/join", dojo.api.ParticipantApiHandler),
            #(r"/user/([A-Za-z_]+)", DojoApiHandler),

            (r"/login/twitter", dojo.auth.TwitterHandler),
            (r"/logout", dojo.auth.LogoutHandler),
            (r"/api/dojo/?([0-9]+)?", dojo.api.DojoApiHandler),
            (r"/api/dojo/([0-9]+)/join", dojo.api.ParticipantApiHandler),

        ]
        settings = dict (
            twitter_consumer_key = options.twitter_consumer_key,
            twitter_consumer_secret = options.twitter_consumer_secret,
            twitter_callback = options.twitter_callback,
            github_client_id = options.github_client_id,
            github_secret = options.github_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug = options.debug,
            cookie_secret = options.cookie_secret,
            login_url = "/login/twitter",
            database_host = options.database_host,
            database_port = options.database_port,
            database_name = options.database_name,
            database_username = options.database_username,
            database_password = options.database_password,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    #logging.info("starting dojo to server") 
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")
    DojoApp(options).listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    
