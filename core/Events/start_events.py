#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：start_events.py
@Author ：Cary
@Date ：2024/2/8 15:21
@Descripttion : "启动事件"
"""
from typing import Callable
from fastapi import FastAPI
from core.Exeption.init import register_exception
from core.Routers.routers_init import register_routers
from extend.datebase.init import register_db
from extend.redis.init import register_redis
from utils.config import settings
from loguru import logger


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        logger.info("FastApi 启动事件监听")

        # 注册自定义错误处理
        await register_exception(app)

        # 注册数据库
        await register_db(app)
        logger.success(f"{settings.DB_ENGINE} 注册完成")

        # 注册redis
        logger.info(f"redis模式 {settings.REDIS_MODE} redis地址 {settings.REDIS_ADDRESS}")
        await register_redis(app)
        logger.success("Redis 注册完成")

        # 注册路由
        await register_routers(app)
        logger.success("Routers 注册完成")

    return app_start
