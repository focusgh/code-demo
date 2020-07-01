#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import asyncio

loop = asyncio.get_event_loop()


# 测试 mysql 异步驱动
db_name = 'master_memorial'
db_user = 'root'
db_pass = '123456'
db_host = '10.2.24.183'
db_port = 51002

from tornado_demo.models.custom_aiomysql import CustomAioMysql
aio_db = CustomAioMysql(
    db_host,
    db_name,
    db_user,
    db_pass,
    # loop=loop,
    port=db_port,
    minsize=4, maxsize=500,
)


async def db_query(sql):
    data = await aio_db.query(sql)
    # print(data)
    return data


async def db_get(sql):
    data = await aio_db.get(sql)
    # print(data)
    return data