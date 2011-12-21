#!/usr/bin/env python
# Xingzhong
#

import os
import datetime
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import dbupdate as myDB

class Account(db.Model):
    account = db.UserProperty()
    port = db.StringListProperty()

class UserHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/user"))

        template_values = {'accounts' : greeting}
        path = os.path.join(os.path.dirname(__file__), 'user.html')
        self.response.out.write(template.render(path, template_values))