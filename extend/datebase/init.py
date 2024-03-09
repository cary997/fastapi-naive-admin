#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：init.py
@Author ：Cary
@Date ：2024/2/3 19:14
@Descripttion : "数据库连接初始化"
"""
from typing import Type

from fastapi import FastAPI
from tortoise import Model
from utils.config import settings
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger


class Router:
    @staticmethod
    def db_for_read(model: Type[Model]):
        return "slave"

    @staticmethod
    def db_for_write(model: Type[Model]):
        return "master"


def format_dblink(engine):
    if engine in ['mysql', 'postgresql']:
        db_urls = {
            "write_url": f'{settings.DB_ENGINE}://{settings.DB_WRITE_URL}',
            "read_url": f'{settings.DB_ENGINE}://{settings.DB_RAER_URL}'
        }
        return db_urls
    elif engine == 'sqlite':
        db_urls = {
            "write_url": f'{settings.DB_ENGINE}:///{settings.BASE_DIR}/fastapi.sqlite',
            "read_url": f'{settings.DB_ENGINE}:///{settings.BASE_DIR}/fastapi.sqlite'
        }
        return db_urls
    else:
        logger.error(f"DB_ENGINE:{settings.DB_ENGINE} 无法识别，请检查数据库配置")
        raise SystemExit('未知数据库类型终止运行')

    # -----------------------数据库配置-----------------------------------


DB_ORM_CONFIG = {
    "connections": {
        'master': format_dblink(settings.DB_ENGINE).get('write_url'),
        'slave': format_dblink(settings.DB_ENGINE).get('read_url'),
    },
    "apps": {
        "models": {
            # "models": ["aerich.models", 'models'],
            "models": ['models'],
            "default_connection": "master"
        },
    },
    "routers": [Router],
    'use_tz': False,
    'timezone': settings.DB_TIMEZONE
}


async def register_db(app: FastAPI):
    # 注册数据库
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=False,
    )
