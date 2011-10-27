# -*- coding: utf-8 -*-

from common import BaseHandler

import tornado.web
import tornado.auth


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
        query = ("INSERT INTO twitterlogins (" +
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
            #TODO, do not update token keys unless it is needed
            query = (
                "UPDATE users SET " +
                "username=%s, " +
                "url=%s, " +
                "twitter_access_token_key=%s, " +
                "twitter_access_token_secret=%s, " +
                "twitter_display_icon=%s " +
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
            try:
                query = (
                    "INSERT INTO users(" +
                    "username, url, twitter_access_token_key, twitter_access_token_secret,"+
                    "twitter_display_icon,  twitter_id" +
                    ") VALUES (%s, %s, %s, %s, %s, %s)"
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
            except TypeError as te:
                log.error("TypeError on the query: " )
                print 'ERROR: '
                print query
                print twitter_user


        db.close()

        #TODO, adicionar data e user_agent
        logged_user = dict(
            id = user_id,
            twitter_id = twitter_user['id'],
            username = twitter_user['username'],
            url = twitter_user['url'],
            twitter_display_icon = twitter_user['profile_image_url'] 
        )
        return logged_user

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")
