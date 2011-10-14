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

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = json_decode(self.get_secure_cookie('user'))
        return user        
    def json_content(self):
        self.set_header('Content-Type', 'application/json')

class PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DashboardApiHandler(BaseHandler):
    
    def get(self, url):
        if url == 'friends':
            #if user has twitter
            self.twitter_request("/followers/ids", 
                access_token= user["access_token"],
                callback= self.async_callback(self._on_followers))
            #if user has facebook
        if url == 'comments':
            #self.twitter.r search twitter by dojo_id
            pass

        
    def _on_friends(self):
        
        pass

    def _on_comments(self):
        pass

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
        db = database.Connection("localhost", "dojo_to")
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

'''
class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        db = database.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title
'''

class DashBoardHandler(BaseHandler, tornado.auth.TwitterMixin):

    #@tornado.web.authenticated
    #@tornado.web.asynchronous
    def get(self):
        user = self.current_user
        self.write(user['username'])
        #self.twitter_request(
        #    "/statuses/update",
        #    post_args={"status": "Testing Tornado Web Server"},
        #    access_token=user["access_token"],
        #    callback=self.async_callback(self._on_post))
        self.twitter_request("/followers/ids",
            access_token= user["access_token"],
            callback= self.async_callback(self._on_followers))
    
    def _on_followers(self, followers):
        print(followers)
        self.finish("aaa")

    def _on_post(self, new_entry):
        if not new_entry:
            # Call failed; perhaps missing permission?
            self.authorize_redirect()
            return
        self.finish("Posted a message!")


class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(callback_uri="http://localhost:8888/login")

    def _on_auth(self, user):
        if not user: raise tornado.web.HTTPError(500, "Twitter auth failed")
        self.set_secure_cookie("username", tornado.escape.json_encode(user))
        db = database.Connection("localhost", "dojo_to")
        query = "SELECT * FROM users WHERE twitter_id %i" % user['twitter_id']
        persistedUser = db.get(query)
        if persistedUser:
            pass
        else:
            pass

        self.redirect("/dashboard")


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
            (r"/dashboard", DashBoardHandler),

        ]
        settings = dict (
            twitter_consumer_key = options.twitter_consumer_key,
            twitter_consumer_secret = options.twitter_consumer_secret,
            github_client_id = options.github_client_id,
            github_secret = options.github_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
            cookie_secret = "dslfkjaslkfjasdflasdf",
            login_url = "/json"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(os.getenv("HOME") + "/dojo_to.conf")
    DojoTo(options).listen(8888)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    
