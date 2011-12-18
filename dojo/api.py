# -*- coding: utf-8 -*-

from common import BaseHandler

import tornado.web
import tornado.auth
from tornado.escape import json_encode, json_decode
import tornado.database

from _mysql_exceptions import DataError

class DojoApiHandler(BaseHandler):
    
    @tornado.web.authenticated
    def post(self, id=None):
        accept_types = self.get_accept_types()
        if 'application/x-www-form-urlencoded' in accept_types:
            dojo = dict (
                user_id = self.get_current_user()['id'],
                language = self.get_argument('language'),
                location = self.get_argument('location'),
                address = self.get_argument('address'),
                city = self.get_argument('city')
            )
            dojo_id = self.create(dojo)
            self.redirect("/dojo/"+ str(dojo_id))
            return
        elif 'application/json' in accept_types:
            dojo = json_decode(self.request.body)
            dojo.setdefault('user_id', self.get_current_user()['id'])
            dojo_id = self.create(dojo)
            self.write(str(dojo_id))
            return
        else:
            print 'error' #throw an error

    def create(self, dojo):
        try:
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
        except DataError:
            pass

    def get(self, id): #restore
        query = (
            "SELECT * FROM dojos WHERE id = %s"
        )
        db = self.get_database()
        dojo = db.get(query, id)
        if not dojo: raise tornado.web.HTTPError(404, "Dojo not found")
        participants = None
        accept_types = self.get_accept_types()
        content = self.render_string('dojo.html', logged_user = self.get_current_user(), dojo = dojo)
        if 'text/html' in accept_types:
            self.render('home.html', content1 = content, content2 = None, logged_user = self.current_user)
            return
        elif 'application/json' in accept_types:
            self.write(json_encode(dojo))
            return
        elif 'ajax/html' in accept_types or self.is_xml_http_request():
            self.write(content)
            return

    def put (self, id): #update
        #self.json_content()
        pass
    def delete(self, id): #delete
        #self.json_content()
        pass


class ParticipantApiHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self, id=None):
        accept_types = self.get_accept_types()
        if 'application/x-www-form-urlencoded' in accept_types:
            #TODO: if dojo event time > 12 horas confimed = False
            participant = dict (
                user_id = self.get_current_user()['id'],
                dojo_id = id,
                confirmed = False,
            )
            self.create(participant)
            self.redirect("/dojo/"+ id)
            return
        elif 'application/json' in accept_types:
            '''
            dojo = json_decode(self.request.body)
            dojo.setdefault('user_id', self.get_current_user()['id'])
            self.create(dojo)
            self.write('ok')
            '''
            return
        else:
            print 'error' #throw an error
    
    def create(self, participant):
        try:
            db = self.get_database()
            query = (
                "INSERT INTO participants ("+
                "user_id, dojo_id) values (%s, %s)"
            )
            participant_id = db.execute_lastrowid(
                query,
                participant['user_id'], participant['dojo_id']
            )
            return participant_id
        except TypeError:
            pass
        finally:
            db.close()
        #except ProgrammingError:
        #pass

class SocialApiHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, url):
        if url == 'friends':
            #if user has twitter
            db = self.get_database()
            #TODO callback database
            private = db.get("SELECT * FROM users WHERE id=%s", self.current_user['id'])
            self.twitter_request("/followers/ids", 
                access_token= private["access_token"],
                callback= self.async_callback(self._on_twitter_friends))
            db.close()
            return
            #if user has facebook
        if url == 'comments':
            #self.twitter.r search twitter by dojo_id
            pass
        
        self.write('ok')
        
    def _on_twitter_friends(self, followers_ids): 
        db = self.getdatabase()
        ids = ','.join(map(str,followers_ids))
        sql = "SELECT username, twitter_display_icon FROM users WHERE twitter_id IN (%s) ORDER BY username"
        db.query(query)
        db.close()
        self.finish()

    def _on_comments(self):
        pass

    @tornado.web.asynchronous
    def post(self, url):
        if url == 'twit':
            self.twitter_request("status/update", 
                status = "aee",
                access_token= private['access_token'],
                callback = self.async_callback(self._on_twit))

    def _on_twit(self, response):
        pass