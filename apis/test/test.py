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
from extend.ldap.auth_mixin import LdapAuthMixin
from schemas.base import BaseResponse
from schemas.system.settings_schema import mailServerSettings, ldapConfig
from schemas.test.test_schemas import testLdapResponse
from extend.sends.send_mail import sys_send_mail

router = APIRouter(prefix='/apitest')


@router.post('/email', summary="邮件测试接口", response_model=BaseResponse)
async def test_email(config: mailServerSettings, receive: str):
    _res = await sys_send_mail(recipients=receive,
                               config=config.model_dump(),
                               body={'title': "测试信息", "message": "测试成功"},
                               subject="配置测试通知", template_name="email.html")
    if _res.get('code'):
        return success(message="Test Success")
    else:
        return fail(message=_res.get('message'))


@router.post('/ldap', summary="ldap测试接口", response_model=testLdapResponse)
async def test_ldap(config: ldapConfig, username: str):
    _config = config.model_dump()
    conn = LdapAuthMixin(**_config)
    _res = conn.search_user(username)
    if not _res.get('code'):
        return fail(message=f"{_res.get('message')}", data=_res.get('data'))
    if len(_res.get('data')) == 0:
        return success(message=f"{_res.get('message')}", data=_res.get('data'))
    attributes = _config.get('attributes')
    _data = _res.get('data')[0].get('attributes')
    _emial = _data.get(attributes.get('email'))
    _phone = _data.get(attributes.get('phone'))
    data = {
        'username': _data.get(attributes.get('username'))[0],
        'nickname': _data.get(attributes.get('nickname'))[0],
        'email': _emial[0] if _emial else None,
        'phone': _phone[0] if _phone else None,
    }

    return success(message="Test Success", data=data)
