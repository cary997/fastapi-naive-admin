#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：login_schema.py
@Author ：Cary
@Date ：2024/2/20 23:32
@Descripttion : ""
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from schemas.base import BaseResponse


class totpResult(BaseModel):
    totp: Optional[bool] = Field(default=False, title="TOTP设置是否开启")
    new: Optional[bool] = Field(default=False, title="用户是否未绑定令牌")
    new_totp: Optional[str] = Field(default=None, title="新生成令牌绑定链接")


class AccessToken(BaseModel):
    access_token: Optional[str] = Field(default=None, title="令牌")
    refresh_token: Optional[str] = Field(default=None, title="刷新令牌")
    expires_in: Optional[int] = Field(default=None, title="过期时间")
    token_type: Optional[str] = Field(default=None, title="令牌类型")
    user_id: Optional[int] = Field(default=None, title="用户ID")
    username: Optional[str] = Field(default=None, title="用户名")
    nickname: Optional[str] = Field(default=None, title="显示名")
    roles: Optional[List] = Field(default=[], title="用户角色列表")


class AccessResponse(BaseResponse):
    data: AccessToken | totpResult
    access_token: Optional[str] = Field(default=None, title="令牌(用于swagger认证)")
    token_type: Optional[str] = Field(default=None, title="令牌类型(用于swagger认证)")


class RefreshToken(BaseModel):
    access_token: Optional[str] = Field(default=None, title="令牌")
    expires_in: Optional[int] = Field(default=None, title="过期时间")
    refresh_token: Optional[str] = Field(default=None, title="刷新令牌")


class RefreshResponse(BaseResponse):
    data: AccessToken


class LoginRequestForm(OAuth2PasswordRequestForm):
    def __init__(
            self,
            grant_type: str = Form(default="password", description="验证方式"),
            username: str = Form(description="账户"),
            password: Optional[str] = Form(description="密码"),
            scope: str = Form(default="", description="作用域"),
            client_id: Optional[str] = Form(default=None),
            client_secret: Optional[str] = Form(default=None),
            totp_code: Optional[str] = Form(default=None, description="totp验证码")
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.totp_code = totp_code
