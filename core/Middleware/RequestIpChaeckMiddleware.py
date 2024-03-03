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

from core.Exeption.Response import fail
from core.Security.auth_ip_check import verify_client_ip, get_client_ip


class RequestIpChaeckMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        判读IP地址是否运行访问实现IP拦截
        :param request:
        :param call_next:
        :return:
        """
        client_ip = await get_client_ip(request)
        state = await verify_client_ip(client_ip)
        if not state:
            logger.error(f'非法IP {client_ip} 已拦截! - {request.method} 403 {request.url}')
            return fail(http_code=403, message=f'非法IP {client_ip}')
        else:
            response = await call_next(request)
            return response
