#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import traceback
import aiomysql
import pymysql

__all__ = [
    "CustomAioMysql"
]


class CustomAioMysql:

    def __init__(self,
                 host,
                 database,
                 user,
                 password,
                 loop=None,
                 minsize=3, maxsize=5,
                 return_dict=True,
                 pool_recycle=7 * 3600,
                 autocommit=True,
                 charset="utf8mb4", **kwargs):

        self.db_args = {
            'host': host,
            'db': database,
            'user': user,
            'password': password,
            'minsize': minsize,
            'maxsize': maxsize,
            'charset': charset,
            'loop': loop,
            'autocommit': autocommit,
            'pool_recycle': pool_recycle,
        }
        if return_dict:
            self.db_args['cursorclass'] = aiomysql.cursors.DictCursor
        if kwargs:
            self.db_args.update(kwargs)
        self.pool = None

    async def init_pool(self):
        """
        初始化连接池
        """
        print("init pool")
        self.pool = await aiomysql.create_pool(**self.db_args)

    async def query(self, query, *parameters, **kwparameters):
        """
        指定查询

        :return [row, ...]
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchall()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchall()
                return ret

    async def get(self, query, *parameters, **kwparameters):
        """
        指定查询

        :return row
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                return ret

    async def execute(self, query, *parameters, **kwparameters):
        """
        执行指定查询语句
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                except Exception:
                    # https://github.com/aio-libs/aiomysql/issues/340
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                return cur.lastrowid
