#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'


import tornado.httpserver
from tornado_demo.app import make_app
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888)
    server.start(1)
    # app.listen(8888)
    IOLoop.current().start()