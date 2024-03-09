#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：cusotm_route.py
@Author ：Cary
@Date ：2024/2/8 23:17
@Descripttion : ""
"""
import gzip
import json
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class CusotmRoute(APIRoute):
    """
    这个类的主要作用，解决fastapi中使用中间件body只能被消费一次的问题
    也就是如果在中间件中读取body会导致请求无法返回response
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 这里可以获取的我们的请求的体的信息----
            body = await request.body()
            if len(body) != 0:
                body = json.loads(body)
            else:
                body = None
            # 下面可以处理我们的响应体的报文信息----
            # 将body添加至scope中
            request.scope.setdefault("request_body", body)
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
