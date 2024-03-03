#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：shutdown_events.py
@Author ：Cary
@Date ：2024/2/8 15:21
@Descripttion : "停止事件"
"""
from typing import Callable
from fastapi import FastAPI
from loguru import logger


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        logger.info("FastApi 关闭事件监听")

        await app.state.cache.close()
        logger.success("Redis 关闭连接")

    return stop_app
