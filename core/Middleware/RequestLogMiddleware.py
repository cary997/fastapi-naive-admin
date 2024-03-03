#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：RequestLogMiddleware.py
@Author ：Cary
@Date ：2024/2/8 17:19
@Descripttion : "打印所有请求日志"
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from loguru import logger

from core.Security.auth_ip_check import get_client_ip


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        记录请求日志 日志打印要在call_next之后
        FastAPI请求和响应的处理顺序为：中间件处理请求-> 路由处理请求-> 路由处理响应->中间件处理响应
        :param request:
        :param call_next:
        :return:
        """
        # request_body是在cusotm_route中将body添加至scope
        body = request.scope.get('request_body')
        client_ip = await get_client_ip(request)
        response = await call_next(request)
        logger.bind(payload=body).debug(
            f"{client_ip} - {request.method} {response.status_code} {request.url}")
        return response
