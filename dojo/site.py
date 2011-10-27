# -*- coding: utf-8 -*-

from common import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        if self.get_argument('_escaped_fragment_', False):
            self.redirect(self.get_argument('_escaped_fragment_'))
            return
        self.render('home.html', content1 = '', content2 = '', logged_user = self.current_user)

class TimelineHandler(BaseHandler):

    def get(self):
        db = self.get_database()
        if self.current_user:
            #friends = 
            pass
        dojos = db.query("SELECT * FROM dojos")
        query = (
            "select p.id, u.id as user_id, d.id as dojo_id, u.username, u.twitter_display_icon, d.language, d.location, d.city " +
            "from participants as p " +
            "inner join (users as u, dojos as d) " + 
            "on (p.user_id = u.id and p.dojo_id = d.id) order by p.created_at limit 15"
        )
        participants = db.query(query)
        query = (
            "select d.id, d.language, d.location, d.city"
        )
        db.close()
        accept_types = self.get_accept_types()
        content = self.render_string('timeline.html', dojos = dojos, participants = participants)
        if 'ajax/html' in accept_types or self.get_argument('_framed', False):
            self.write(content)
        elif 'application/json' in accept_types:
            pass
        elif 'text/html' in accept_types:
            self.render('home.html', content1 = content, content2 = '', logged_user = self.current_user)
