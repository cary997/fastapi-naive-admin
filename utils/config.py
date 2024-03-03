#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：config.py
@Author ：Cary
@Date ：2024/2/3 19:18
@Descripttion : "加载所有配置"
"""
import os
from pathlib import PosixPath, WindowsPath

from utils.config_yaml_load import BASE_DIR, load
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional, List, Union

# 加载config.yaml配置
DefaultConfig = load()


class Config(BaseSettings):
    """
    默认读取系统环境变量，若无对应key则使用config.yaml中配置
    """
    # 项目根路径
    BASE_DIR: Optional[Union[PosixPath, WindowsPath]] = BASE_DIR
    BASE_TEMPLATES_DIR: Optional[Union[PosixPath, WindowsPath]] = BASE_DIR / 'templates'

    # FastAPI配置
    SYS_TITLE: Optional[str] = DefaultConfig['SYSTEM']['SYS_TITLE']
    SYS_LINK: Optional[str] = DefaultConfig['SYSTEM']['SYS_LINK']
    SYS_DESCRIOTION: Optional[str] = DefaultConfig['SYSTEM']['SYS_DESCRIOTION']
    SYS_VERSION: Optional[str] = DefaultConfig['SYSTEM']['SYS_VERSION']
    SYS_ROUTER_PREFIX: Optional[str] = DefaultConfig['SYSTEM']['SYS_ROUTER_PREFIX']
    SYS_ROUTER_AUTH2: Optional[str] = DefaultConfig['SYSTEM']['SYS_ROUTER_AUTH2']
    SYS_ROUTER_REFRESH: Optional[str] = DefaultConfig['SYSTEM']['SYS_ROUTER_REFRESH']
    SYS_ROUTER_SYNCROUTES: Optional[str] = DefaultConfig['SYSTEM']['SYS_ROUTER_SYNCROUTES']
    SYS_OPENAPI_URL: Optional[str] = DefaultConfig['SYSTEM']['SYS_OPENAPI_URL']

    # 跨域配置
    CORS_ORIGINS: Optional[List] = DefaultConfig['CORS']['CORS_ORIGINS']
    CORS_ALLOW_CREDENTIALS: Optional[bool] = DefaultConfig['CORS']['CORS_ALLOW_CREDENTIALS']
    CORS_ALLOW_METHODS: Optional[List] = DefaultConfig['CORS']['CORS_ALLOW_METHODS']
    CORS_ALLOW_HEADERS: Optional[List] = DefaultConfig['CORS']['CORS_ALLOW_HEADERS']

    # 日志配置
    LOG_PATH: Optional[str] = DefaultConfig['LOG']['LOG_PATH']
    ORM_LOG_PATH: Optional[str] = DefaultConfig['LOG']['ORM_LOG_PATH']
    LOG_FORMAT: Optional[str] = DefaultConfig['LOG']['LOG_FORMAT']
    LOG_LEVER: Optional[str] = DefaultConfig['LOG']['LOG_LEVER']
    LOG_ROTATION_TIME: Optional[str] = DefaultConfig['LOG']['LOG_ROTATION_TIME']
    LOG_ROTATION_SIZE: Optional[str] = DefaultConfig['LOG']['LOG_ROTATION_SIZE']
    LOG_RETENTION: Optional[str] = DefaultConfig['LOG']['LOG_RETENTION']
    LOG_CONSOLE: Optional[bool] = DefaultConfig['LOG']['LOG_CONSOLE']
    LOG_FILE: Optional[bool] = DefaultConfig['LOG']['LOG_FILE']

    # 安全配置
    SECRET_KEY: Optional[str] = DefaultConfig['SECURITY']['SECRET_KEY']
    SECRET_IV: Optional[str] = DefaultConfig['SECURITY']['SECRET_IV']
    SECRET_JWT_KEY: Optional[str] = DefaultConfig['SECURITY']['SECRET_JWT_KEY']
    SECRET_JWT_ALGORITHM: Optional[str] = DefaultConfig['SECURITY']['SECRET_JWT_ALGORITHM']
    SECRET_JWT_EXP: Optional[int] = DefaultConfig['SECURITY']['SECRET_JWT_EXP']
    SECRET_REJWT_EXP: Optional[int] = DefaultConfig['SECURITY']['SECRET_REJWT_EXP']

    # 数据库配置
    DB_ENGINE: Optional[str] = DefaultConfig['DATABASE']['DB_ENGINE']
    DB_WRITE_URL: Optional[str] = DefaultConfig['DATABASE']['DB_WRITE_URL']
    DB_RAER_URL: Optional[str] = DefaultConfig['DATABASE']['DB_RAER_URL']
    DB_TIMEZONE: Optional[str] = DefaultConfig['DATABASE']['DB_TIMEZONE']

    # redis配置
    REDIS_MODE: Optional[str] = DefaultConfig['CACHE']['REDIS_MODE']
    REDIS_DB: Optional[int] = DefaultConfig['CACHE']['REDIS_DB']
    REDIS_ADDRESS: Optional[str] = DefaultConfig['CACHE']['REDIS_ADDRESS']
    REDIS_USERNAME: Optional[str] = DefaultConfig['CACHE']['REDIS_USERNAME']
    REDIS_PASSWORD: Optional[str] = DefaultConfig['CACHE']['REDIS_PASSWORD']
    REDIS_SENTINEL_NAME: Optional[str] = DefaultConfig['CACHE']['REDIS_SENTINEL_NAME']
    REDIS_ENCODING: Optional[str] = DefaultConfig['CACHE']['REDIS_ENCODING']
    REDIS_MAX_CONNECTIONS: Optional[int] = DefaultConfig['CACHE']['REDIS_MAX_CONNECTIONS']
    REDIS_SSL: Optional[bool] = DefaultConfig['CACHE']['REDIS_SSL']
    REDIS_SSL_CERT_REQS: Optional[str] = DefaultConfig['CACHE']['REDIS_SSL_CERT_REQS']
    REDIS_SSL_CA_CERTS: Optional[str] = DefaultConfig['CACHE']['REDIS_SSL_CA_CERTS']

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        case_sensitive = True
        env_prefix = "FASTAPI_"


# 缓存配置信息
@lru_cache
def get_settings():
    return Config()


# 配置文件实例化
settings = get_settings()

if __name__ == "__main__":
    print(settings.dict())
