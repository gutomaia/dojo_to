# -*- coding: utf-8 -*-

from common import BaseHandler
import api

class Home(BaseHandler):
    def get(self):
        if self.get_argument('_escaped_fragment_', False):
            self.redirect(self.get_argument('_escaped_fragment_'))
            return
        self.render('home.html', content1 = '', content2 = '', logged_user = self.current_user)


class Timeline(BaseHandler):

    def get(self, type = 'public'):
        db = self.get_database()
        fields = (
            "SELECT p.id, u.id as user_id, d.id as dojo_id, " +
            "u.username, u.twitter_display_icon, " +
            "d.language, d.location, d.city")
        tables = (" FROM participants as p " +
                "inner join (users as u, dojos as d) " + 
                "on (p.user_id = u.id and p.dojo_id = d.id)")
        orderby = " order by p.created_at limit 15"
        if type == 'of_friends':
            #if not self.current_user
            userlist =','.join(map(str,list))
            where = " WHERE u.twitter_id in (%s)" % userlist
            query = (fields + tables + where + orderby)
        if type == 'public':
            query = (fields + tables + orderby)            
        participants = db.query(query)
        db.close()
        accept_types = self.get_accept_types()
        content = self.render_string('timeline.html', participants = participants, logged_user = self.current_user)
        if 'ajax/html' in accept_types or self.get_argument('_framed', False):
            self.write(content)
        elif 'application/json' in accept_types:
            pass
        elif 'text/html' in accept_types:
            self.render('home.html', content1 = content, content2 = '', logged_user = self.current_user)

class Dojos(BaseHandler):
    def get(self):
        db = self.get_database()
        dojos = db.query("SELECT * FROM dojos")
        accept_types = self.get_accept_types()
        content = self.render_string("dojos.html", dojos = dojos)
        if 'ajax/html' in accept_types or self.get_argument('_framed', False):
            self.write(content)
        elif 'application/json' in accept_types:
            pass
        elif 'text/html' in accept_types:
            self.render('home.html', content1 = content, content2 = '', logged_user = self.current_user)

class Dojo(BaseHandler):

    def get(self, language=None, city=None):
        content = language
        accept_types = self.get_accept_types()
        if 'ajax/html' in accept_types:
            self.write(content)
        elif 'application/json' in accept_types:
            pass
        elif 'text/html' in accept_types:
            self.render('home.html', content1 = content, content2 = '', logged_user = self.current_user)

class User(BaseHandler):

    def get(self, username):
        db = self.get_database()
        user = db.get('SELECT * FROM user WHERE username=%s', username)
                
        #content = self.render_string('user.html', participants = participants)
        accept_types = self.get_accept_types()
        if 'ajax/html' in accept_types:
            self.write(content)
