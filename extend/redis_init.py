#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：redis_init.py
@Author ：Cary
@Date ：2024/2/26 14:27
@Descripttion : "redis连接初始化"
"""
from typing import Union, Annotated

from pydantic import Field
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.requests import Request

from utils.config import settings
from loguru import logger


class RedisMinx:
    def __init__(self):
        self.mode: str = settings.REDIS_MODE
        self.host: str = settings.REDIS_ADDRESS
        self.db: int = settings.REDIS_DB
        self.username: str = settings.REDIS_USERNAME
        self.password: str = settings.REDIS_PASSWORD
        self.sentinel_name: str = settings.REDIS_SENTINEL_NAME
        self.encoding: str = settings.REDIS_ENCODING
        self.decode_responses: bool = True
        self.max_connections: int = settings.REDIS_MAX_CONNECTIONS
        self.ssl: bool = settings.REDIS_SSL
        self.ssl_cert_reqs: str = settings.REDIS_SSL_CERT_REQS
        self.ssl_ca_certs: str = settings.REDIS_SSL_CA_CERTS

    @property
    async def redis_standalone_conn(self) -> aioredis.Redis:
        """
        单机
        :return:
        """
        return aioredis.Redis(host=self.host.split(":")[0], port=int(self.host.split(":")[-1]), username=self.username,
                              password=self.password, db=self.db, decode_responses=self.decode_responses,
                              max_connections=self.max_connections, ssl=self.ssl, ssl_cert_reqs=self.ssl_cert_reqs,
                              ssl_ca_certs=self.ssl_ca_certs)

    @property
    async def redis_sentinel_conn(self) -> aioredis.Sentinel:
        """
        哨兵
        :return:
        """
        sentinel_list = []
        for address in self.host.split(','):
            sentinel_host = address.split(':')[0]
            sentinel_port = address.split(':')[-1]
            sentinel_list.append((
                sentinel_host, sentinel_port
            ))
        return aioredis.Sentinel(sentinels=sentinel_list, username=self.username,
                                 password=self.password, db=self.db, decode_responses=self.decode_responses,
                                 max_connections=self.max_connections, ssl=self.ssl, ssl_cert_reqs=self.ssl_cert_reqs,
                                 ssl_ca_certs=self.ssl_ca_certs)

    @property
    async def redis_cluster_conn(self) -> aioredis.RedisCluster:
        """
        集群
        :return:
        """
        startup_nodes = []
        for address in self.host.split(','):
            startup_nodes.append(aioredis.cluster.ClusterNode(address.split(":")[0], address.split(":")[-1]))
        return aioredis.RedisCluster(startup_nodes=startup_nodes, username=self.username, password=self.password,
                                     decode_responses=self.decode_responses, ssl=self.ssl,
                                     ssl_cert_reqs=self.ssl_cert_reqs,
                                     ssl_ca_certs=self.ssl_ca_certs)

    @property
    async def connect_redis(self):
        """
        连接redis
        """

        if self.mode == "standalone":
            redis_conn: aioredis.Redis = await self.redis_standalone_conn
        elif self.mode == "sentinel":
            redis_conn: aioredis.Sentinel = await self.redis_sentinel_conn
        elif self.mode == "cluster":
            redis_conn: aioredis.RedisCluster = await self.redis_cluster_conn
        else:
            raise ValueError("Redis mode not supported")
        try:
            await redis_conn.ping()
        except aioredis.ConnectionError as e:
            raise ConnectionError(f"Redis连接失败 - {e}")
        return redis_conn


async def register_redis(app: FastAPI):
    # 注册redis测试连接
    app.state.cache = await RedisMinx().connect_redis


redisCache = Annotated[Union[aioredis.Redis, aioredis.Sentinel, aioredis.RedisCluster], Field(description="redis联合类型")]


async def get_redis() -> redisCache:
    _redis_coon = await RedisMinx().connect_redis
    return _redis_coon


if __name__ == "__main__":
    import asyncio

    a = asyncio.run(RedisMinx().connect_redis)
    print(type(a))
    print(a)
