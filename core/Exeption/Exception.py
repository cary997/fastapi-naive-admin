# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: 异常处理
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Union, Dict
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, BaseModel, Field
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError as MysqlValidationError
from loguru import logger


async def mysql_validation_error(_: Request, exc: MysqlValidationError):
    """
    数据库字段验证错误
    :param _:
    :param exc:
    :return:
    """
    logger.debug(f"ValidationError - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.__str__(),
        "data": []
    }, status_code=422)


async def mysql_integrity_error(_: Request, exc: IntegrityError):
    """
    完整性错误
    :param _:
    :param exc:
    :return:
    """
    logger.debug(f"IntegrityError - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.__str__(),
        "data": []
    }, status_code=422)


async def mysql_does_not_exist(_: Request, exc: DoesNotExist):
    """
    mysql 查询对象不存在异常处理
    :param _:
    :param exc:
    :return:
    """
    logger.debug(f"DoesNotExist - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.__str__(),
        "data": []
    }, status_code=404)


async def mysql_operational_error(_: Request, exc: OperationalError):
    """
    mysql 数据库异常错误处理
    :param _:
    :param exc:
    :return:
    """
    logger.debug(f"OperationalError - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.__str__(),
        "data": []
    }, status_code=500)


async def http_error_handler(_: Request, exc: HTTPException):
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """

    logger.debug(f"HTTPException - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.detail,
        "data": exc.headers
    }, status_code=exc.status_code, headers=exc.headers)


class UnicornException(Exception):

    def __init__(self, errmsg, data=None):
        """
        失败返回格式
        :param errmsg:
        """
        if data is None:
            data = {}
        self.code = 0
        self.errmsg = errmsg
        self.data = data


async def unicorn_exception_handler(_: Request, exc: UnicornException):
    """
    unicorn 异常处理
    :param _:
    :param exc:
    :return:
    """

    logger.debug(f"UnicornException - {exc}")
    return JSONResponse({
        "code": 0,
        "message": exc.errmsg,
        "data": exc.data,
    })


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
    """
    参数校验错误处理
    :param _:
    :param exc:
    :return:
    """
    logger.debug(f"ValidationError - {exc}")
    return JSONResponse(
        {
            "code": 0,
            "message": "数据校验错误",
            "data": exc.errors(),
        },
        status_code=422,
    )


class Http422ErrorResponse(BaseModel):
    code: int = Field(title="状态码")
    message: str = Field(title="提示信息")
    data: Dict = Field(title="错误信息", default={
        "detail": [
            {
                "loc": [
                    "string",
                    "string"
                ],
                "msg": "string",
                "type": "string"
            }
        ]
    })
