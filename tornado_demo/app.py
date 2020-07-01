#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'
from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.ioloop import IOLoop

from tornado_demo.views import MainHandler
from tornado_demo.views import PerformanceTest
# from motor.motor_tornado import MotorClient
# connection = MotorClient(
#     # 'master_memorial',
#     # alias='mongo',
#     host='10.2.24.183',
#     port=31000,
#     username='siteRootAdmin',
#     password='mongodb_password',
#     # authentication_source="admin"
# )

from pymongo import MongoClient
connection = MongoClient(
    # 'master_memorial',
    # alias='mongo',
    host='10.2.24.183',
    port=31000,
    username='siteRootAdmin',
    password='mongodb_password',
    # authentication_source="admin"
)

db_conn = connection['master_memorial']


SETTINGS = {
    "debug": True,
    "db_conn": db_conn,
}


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ptest/", PerformanceTest),
        ],
        **SETTINGS
    )


if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(1)
    # app.listen(8888)
    IOLoop.current().start()