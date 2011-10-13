# -*- coding: utf-8 -*-

import os, os.path, sys, urllib

import tornado.ioloop
import tornado.web
import tornado.auth

from tornado.template import Template
from tornado.escape import json_encode, json_decode
from tornado.options import define, options

from tornado import httpclient

class BaseHandler(tornado.web.RequestHandler):
    #def get_current_user(self):
        #user = json_decode(self.get_secure_cookie('user'))
        #return user
        
    def json_content(self):
        self.set_header('Content-Type', 'application/json')

class PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DashboardApiHandler(BaseHandler):
    
    def get(self, url):
        if url == 'friends':
            self.twitter_request("/followers/ids", 
                access_token= user["access_token"],
                callback= self.async_callback(self._on_followers))
        if url == 'comments':
            pass

    def _on_friends(self):
        
        pass

    def _on_comments(self):
        pass



class OrganizeADojoHandler(BaseHandler):
    
    #@tornado.web.authenticated
    #@tornado.web.asynchronous
    def post(self): #create
        #self.json_content()
        pass 
    def get(self): #restore
        #self.json_content()
        self.write(json_encode(crud.restore()))
        pass
    def put (self): #update
        #self.json_content()
        pass
    def delete(self): #delete
        #self.json_content()
        pass

class DojoCrud(object):
    def create(self):
        pass
    def restore(self):
        pass
    def update(self):
        pass
    def delete(self):
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
        self.redirect("/dashboard")
 


class DojoTo(tornado.web.Application):
    def __init__(self, options):
        handlers = [
            (r"/", PageHandler),
            #(r"/learn/", PageHandler),
            (r"/login/twitter", TwitterHandler),
            (r"/api/dojo/([0-9]*)",OrganizeADojoHandler),
            (r"/api/dojo/([0-9]/join)", OrganizeADojoHandler),
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
    
