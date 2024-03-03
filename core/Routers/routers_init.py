#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：routers_init.py
@Author ：Cary
@Date ：2024/2/6 02:05
@Descripttion : ""
"""
from fastapi import FastAPI
from loguru import logger
from fastapi.routing import APIRoute

from core.Routers.routers import Routers


async def register_routers(app: FastAPI):
    """
    自动注册路由
    :param app: FastAPI 实例对象 或者 APIRouter对象
    :return: 默认None
    """
    app.include_router(Routers)
    for route in app.routes:
        try:
            # 为所有route添加ID
            if isinstance(route, APIRoute):
                route.operation_id = route.name
        except AttributeError as e:
            logger.error(f" {e} ")
