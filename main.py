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

from user import UserHandler
import dbupdate as myDB
import parse as myParse

class Equity(db.Model):
    ticker = db.StringProperty(required=True)
    style  = db.BooleanProperty(required=True)
    target = db.FloatProperty(required=True)
    price  = db.FloatProperty(required=True)
    date   = db.DateProperty(auto_now_add=True)
    maturity = db.DateProperty(required=True)


class MainHandler(webapp.RequestHandler):
    def get(self):
        debug  = "debug"
        #debug = cgi.escape(myParse.Parser("AAPL").debug())
        myDB.update(['A'], [datetime.date(2012, 2, 1)])
        equitys = db.GqlQuery("SELECT * FROM Equity Where ticker = :1 ORDER BY target DESC", 'A')
        template_values ={"debug":debug, "equitys": equitys}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))



def main():
    application = webapp.WSGIApplication(\
                                            [('/', MainHandler),\
                                            ('/user', UserHandler)],\
                                        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
