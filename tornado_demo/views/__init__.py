#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'
from typing import Optional, Awaitable

import tornado.web
from tornado import gen
from tornado.escape import json_encode

from tornado_demo.models import (
    loop,
    db_query
)
# import nest_asyncio
# nest_asyncio.apply()


class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.write("hello world.")

    def post(self):
        req = self.request
        print(req)
        res = self.request.body_arguments
        print(res)
        self.write("hello world. post request.")


# async def do_find_one(**kwargs):
#     document = await db_conn.workflow_log.find_one(kwargs)
#     return document

class PerformanceTest(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def get(self):
        print("==>> get")
        db_conn = self.settings['db_conn']
        document = await db_conn.workflow_log.find_one({"log_id": 39425})
        result = {
            "data": document.get("content")
        }
        self.write(result)

    # @gen.coroutine
    def post(self):
        print("==>> post")
        # sql = "SELECT id from job where status = 0 limit 10;"
        #
        # print(loop)
        # result = loop.run_until_complete(db_query(sql))
        # document = yield tornado.gen.Task(db_conn.workflow_log.find_one({"log_id": 39425}))
        db_conn = self.settings['db_conn']
        document = db_conn.workflow_log.find_one({"log_id": 39425})
        # document = yield db_conn.workflow_log.find_one({"log_id": 39425})
        # document = yield gen.sleep(3)
        # document = yield self.find_one()
        result = {
            "data": document.get("content")
        }
        # return result
        self.write(result)
        # self.finish()

    # @gen.coroutine
    # def find_one(self):
    #     document = yield db_conn.workflow_log.find_one({"log_id": 39425})
    #     return document
