#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastcow-server
@File ：test.py
@Author ：Cary
@Date ：2024/3/3 8:21
@Descripttion : ""
"""
from fastapi import APIRouter

from core.Exeption.Response import success, fail
from schemas.base import BaseResponse
from schemas.system.settings_schema import mailServerSettings
from utils.send_tools.send_mail import sys_send_mail

router = APIRouter(prefix='/apitest')


@router.post('/email', summary="邮件测试接口", response_model=BaseResponse)
async def test_email(config: mailServerSettings, receive: str):
    _res = await sys_send_mail(recipients=receive,
                               config=config.model_dump(),
                               body={'title': "测试信息", "message": "测试成功"},
                               subject="配置测试通知", template_name="system-info.html")
    if _res.get('code'):
        return success(message="Test Success")
    else:
        return fail(message=_res.get('message'))
