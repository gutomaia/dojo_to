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

define("port", help="Application Port", default=8888)

define("cookie_secret", help="App Cookie Secret")

define("debug", help="App Debug", default=False)

define("database_host", help="Database host", default="localhost")
define("database_port", help="Database port", default=3306)
define("database_name", help="Database name", default="dojo_to")
define("database_username", help="Database username", default="dojo_to")
define("database_password", help="Database password", default=None)

define("twitter_consumer_key", help="your Twitter application API key")
define("twitter_consumer_secret", help="your Twitter application secret")
define("twitter_callback", help="your twitter callback", default=None)

define("github_client_id", help="your Github application client id")
define("github_secret", help="your Github application secret")


class BaseHandler(tornado.web.RequestHandler):

    #def __init__(self, request, **kwargs):
    #    self.require_setting('cookie_secret')
    #    self.require_setting('cookie_sec')
    #super(BaseHandler, self, request **kwargs)

    def get_database(self):
        db = database.Connection(
            self.settings['database_host'],
            self.settings['database_name']
        )
        return db


    def get_current_user(self):
        if self.get_cookie('user'): #TODO check for a non-secure-cookie
            print 'user logged'
            return json_decode(self.get_secure_cookie('user'))
        print 'user not logged'
        return None

    def json_content(self):
        self.set_header('Content-Type', 'application/json')

class PageHandler(BaseHandler):

    def get(self):
        db = self.get_database()
        if self.current_user:
            print 'aaa aads asddasd';
        #db = self.get_database()
        dojos = db.query("SELECT * FROM dojos")
        query = (
            "select p.id, u.id, d.id, u.username, u.twitter_display_icon, d.language, d.location, d.city " +
            "from participants as p " +
            "inner join (users as u, dojos as d) " + 
            "on (p.user_id = u.id and p.dojo_id = d.id) order by p.created_at"
        )
        participants = db.query(query)
        query = (
            "select d.id, d.language, d.location, d.city"
        )
        db.close()
        self.render('index.html', dojos = participants, logged_user = self.current_user)

        

class DojoPageHandler(BaseHandler):

    def get(self, language=None, city=None):
        self.write(language)

class DojoApiHandler(BaseHandler):
    
    #@tornado.web.authenticated
    #@tornado.web.asynchronous
    def post(self, id): #create
        self.write('post')
        arg = self.request.arguments
        user_id = self.get_argument('user_id')
        local = arg['local']
        db = self.get_database()
        query = "INSERT INTO dojos (user_id) VALUES (%s)"
        dojo_id = db.execute_lastrowid(query, user_id)
        if dojo_id:
            self.redirect("/dojo/"+ str(dojo_id))
            #pass

        #self.json_content()
    def get(self, id): #restore
        self.write('get')
        #self.json_content()
        #self.write(json_encode(crud.restore()))
        pass
    def put (self, id): #update
        #self.json_content()
        pass
    def delete(self, id): #delete
        #self.json_content()
        pass

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

class LogoutHandler(BaseHandler):
    pass

class TwitterHandler(BaseHandler, tornado.auth.TwitterMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(callback_uri="http://localhost:8888/login/twitter")

    def _on_auth(self, user):
        if not user: raise tornado.web.HTTPError(500, "Twitter auth failed")
        print 'cookie seted'
        db = self.get_database()
        query = "SELECT * FROM users WHERE twitter_id = %s or username = %s LIMIT 1"
        pUser = db.get(query, user['id'], user['username'])
        if pUser:
            query = "UPDATE users SET username=%s, twitter_access_token_key=%s, twitter_display_icon=%s where twitter_id=%s"
            db.execute(query, user['username'], "asdf", user['profile_image_url'], user['id'])
        else:
            #IntegrityError
            query = "INSERT INTO users(username, twitter_id, twitter_access_token_key, twitter_display_icon) VALUES (%s, %s, %s, %s)"
            db.execute(query, user['username'], user['id'], "asdf", user['profile_image_url'])
        del user['status']
        del user['access_token']
        self.set_secure_cookie('user', json_encode(user))    
        self.redirect("/")

    def _on_register(self, user):
        db.execute() 


class DojoTo(tornado.web.Application):
    def __init__(self, options):
        handlers = [
            (r"/", PageHandler),
            (r"/learn/([A-Za-z_]+)", DojoPageHandler),
            (r"/learn/([A-Za-z_]+)/in/([A-Za-z_]+)", DojoPageHandler),
            (r"/login/twitter", TwitterHandler),
            (r"/api/dojo/?([0-9]+)?", DojoApiHandler),
            (r"/api/dojo/([0-9]/join)", DojoApiHandler),

        ]
        settings = dict (
            twitter_consumer_key = options.twitter_consumer_key,
            twitter_consumer_secret = options.twitter_consumer_secret,
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
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(os.getenv("HOME") + "/.dojo_to.conf")

    DojoTo(options).listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    
