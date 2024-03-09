#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：test_schemas.py
@Author ：Cary
@Date ：2024/3/5 5:09
@Descripttion : ""
"""
from typing import Optional

from pydantic import Field, BaseModel

from schemas.base import BaseResponse


class ldapSearchUserResults(BaseModel):
    username:str = Field(default=None, description='用户名')
    nickname:str = Field(default=None, description='显示名')
    email:str = Field(default=None, description='邮箱')
    phone:str = Field(default=None, description='手机')


class testLdapResponse(BaseResponse):
    data: Optional[ldapSearchUserResults] = None
