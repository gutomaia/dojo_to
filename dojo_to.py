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
define("database_username", help="Database username", default=None)
define("database_password", help="Database password", default=None)

define("twitter_consumer_key", help="your Twitter application API key")
define("twitter_consumer_secret", help="your Twitter application secret")
define("twitter_callback", help="your twitter callback", default=None)

define("github_client_id", help="your Github application client id")
define("github_secret", help="your Github application secret")


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
        print "call"
        if self.get_cookie('user'): #TODO check for a non-secure-cookie
            return json_decode(self.get_secure_cookie('user'))
        return None

    def json_content(self):
        self.set_header('Content-Type', 'application/json')

class PageHandler(BaseHandler):

    def get(self):
        db = self.get_database()
        if self.current_user:
            #friends = 
            pass
        dojos = db.query("SELECT * FROM dojos")
        query = (
            "select p.id, u.id, d.id, u.username, u.twitter_display_icon, d.language, d.location, d.city " +
            "from participants as p " +
            "inner join (users as u, dojos as d) " + 
            "on (p.user_id = u.id and p.dojo_id = d.id) order by p.created_at limit 15"
        )
        participants = db.query(query)
        query = (
            "select d.id, d.language, d.location, d.city"
        )
        db.close()
        self.render('index.html', dojos = dojos, participants = participants, logged_user = self.current_user)

class DojoPageHandler(BaseHandler):

    def get(self, language=None, city=None):
        self.write(language)

class CrudDojoHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, id = None):
        if (id):
            pass
        self.render('dojo_form.html', dojo=dojo, logged_user = self.current_user)
        pass

class DojoApiHandler(BaseHandler):
    
    @tornado.web.authenticated
    def post(self, id=None):
        content_type = self.request.headers['Content-Type']
        if content_type == 'application/x-www-form-urlencoded':
            dojo = dict (
                user_id = 1,
                language = self.get_argument('language'),
                location = self.get_argument('location'),
                address = self.get_argument('address'),
                city = self.get_argument('city')
            )
            dojo_id = self.create(dojo)
            self.redirect("/dojo/"+ str(dojo_id))
            return
        elif content_type == 'application/json':
            dojo = json_decode(self.request.body)
            dojo.setdefault('user_id', 1)
            dojo_id = self.create(dojo)
            self.write(str(dojo_id))
            return
        else:
            print 'error'

    def create(self, dojo):
        db = self.get_database()
        query = (
            "INSERT INTO dojos ("+
            "user_id, language, location, address, city"+
            ") values (%s, %s, %s, %s, %s)"
        )
        dojo_id = db.execute_lastrowid(
            query,
            dojo['user_id'], dojo['language'], dojo['location'],
            dojo['address'], dojo['city']
        )
        db.close()
        return dojo_id

    def get(self, id): #restore
        query = (
            "SELECT * FROM dojos WHERE id = %s"
        )

        if content_type == 'text/html':
            dojo = dict (
                user_id = 1,
                language = self.get_argument('language'),
                location = self.get_argument('location'),
                address = self.get_argument('address'),
                city = self.get_argument('city')
            )
            dojo_id = self.create(dojo)
            self.redirect("/dojo/"+ str(dojo_id))
            return
        elif content_type == 'application/json':
            pass


    def restore(self, dojo_id):
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

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class TwitterHandler(BaseHandler, tornado.auth.TwitterMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(callback_uri = self.settings['twitter_callback'])

    def _on_auth(self, user):
        if not user: raise tornado.web.HTTPError(500, "Twitter auth failed")
        logged_user = self.register(user)
        query = ("INSERT INTO twitterlogins ("
            "user_id, username, twitter_id," +
            "protected, following, " +
            "friends_count, " + "followers_count, " +
            "favourites_count, listed_count, status_count, " + 
            "geo_enabled, location, coordinates, " +
            "time_zone, lang"+
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        self.set_secure_cookie('user', json_encode(logged_user))    
        self.redirect("/")

    def register(self, twitter_user):
        db = self.get_database()
        query = "SELECT * FROM users WHERE twitter_id = %s LIMIT 1"
        user = db.get(query, twitter_user['id'])
        if user:
            user_id = user['id']
            query = (
                "UPDATE users SET " +
                "username=%s, " +
                "url=%s, " +
                "twitter_access_token_key=%s, " +
                "twitter_access_token_secret=%s, " +
                "twitter_display_icon=%s "+
                "where twitter_id=%s"
            )
            db.execute(
                query,
                twitter_user['username'],
                twitter_user['url'],
                twitter_user['access_token']['key'],
                twitter_user['access_token']['secret'],
                twitter_user['profile_image_url'],
                twitter_user['id']
            )
        else:
            query = (
                "INSERT INTO users(" +
                "username, url, twitter_access_token_key, twitter_access_token_secret,"+
                "twitter_display_icon,  twitter_id" +
                ") VALUES (%s, %s, %s, %s)"
            )
            user_id = db.execute_lastrowid(
                query, 
                twitter_user['username'],
                twitter_user['url'],
                twitter_user['access_token']['key'],
                twitter_user['access_token']['secret'],
                twitter_user['profile_image_url'],
                twitter_user['id']
            )
        db.close()

        logged_user = dict(
            id = user_id,
            twitter_id = twitter_user['id'],
            username = twitter_user['username'],
            url = twitter_user['url'],
            twitter_display_icon = twitter_user['profile_image_url'] 
        )
        return logged_user


class DojoTo(tornado.web.Application):
    def __init__(self, options):
        handlers = [
            (r"/", PageHandler),
            (r"/learn/([A-Za-z_]+)", DojoPageHandler),
            (r"/learn/([A-Za-z_]+)/in/([A-Za-z_]+)", DojoPageHandler),
            (r"/login/twitter", TwitterHandler),
            (r"/logout", LogoutHandler),
            (r"/api/dojo/?([0-9]+)?", DojoApiHandler),
            (r"/api/dojo/([0-9]/join)", DojoApiHandler),

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

    DojoTo(options).listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    
