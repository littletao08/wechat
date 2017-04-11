#-*- coding:utf-8 -*-

from manager import app

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
