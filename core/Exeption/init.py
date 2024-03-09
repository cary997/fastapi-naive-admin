#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：init.py
@Author ：Cary
@Date ：2024/2/25 3:55
@Descripttion : ""
"""

# 注册中间件
from fastapi import FastAPI
from tortoise.exceptions import DoesNotExist, OperationalError, IntegrityError, ValidationError
from core.Exeption import Exception
from fastapi.exceptions import RequestValidationError, HTTPException


async def register_exception(app: FastAPI):
    # 异常错误处理
    app.add_exception_handler(HTTPException, Exception.http_error_handler)
    app.add_exception_handler(RequestValidationError, Exception.http422_error_handler)
    app.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)
    app.add_exception_handler(DoesNotExist, Exception.mysql_does_not_exist)
    app.add_exception_handler(IntegrityError, Exception.mysql_integrity_error)
    app.add_exception_handler(ValidationError, Exception.mysql_validation_error)
    app.add_exception_handler(OperationalError, Exception.mysql_operational_error)