#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：settings_schema.py
@Author ：Cary
@Date ：2024/2/26 22:15
@Descripttion : ""
"""
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from extend.ldap.auth_mixin import attributesMap
from models.system.model import SystemSettings
from schemas.base import BaseResponse

# 用于序列化返回结果
from utils.password_tools import aes_hash_password

SystemSettingsResult = pydantic_model_creator(
    cls=SystemSettings,
    name="SystemSettingsResult",
)


class watermarkContentEnum(IntEnum):
    username = 1
    nickname = 2
    username_nickname = 3


class watermarkSizeEnum(IntEnum):
    compact = 1
    default = 2
    loose = 3


class generalSettings(BaseModel):
    user_default_password: Optional[str] = Field(default=aes_hash_password("FastApi@2024"), description="用户创建时静态密码")
    user_default_roles: Optional[List[int]] = Field(default=[], description="用户默认角色")
    watermark: Optional[bool] = Field(default=False, description="是否开启水印")
    watermarkContent: Optional[watermarkContentEnum] = Field(default=1, description="水印内容")
    watermarkSize: Optional[watermarkSizeEnum] = Field(default=2, description="水印大小")


class ldapConfig(BaseModel):
    enable: Optional[bool] = Field(default=False, description="开启LDAP登录")
    hosts: Optional[List[str]] = Field(default=None, description="ldap server列表")
    user: Optional[str] = Field(default=None, description="用于连接ldap 的user dn")
    password: Optional[str] = Field(default=None, description="用于连接ldap 的user password")
    base_ou: Optional[str] = Field(default=None, description="搜索起始的OU")
    attributes: attributesMap = Field(default=attributesMap(), description="ldap与平台用户字段映射")
    paged_size: Optional[int] = Field(default=500, lt=1000, description="查询分页数")


class ldapSyncEnum(IntEnum):
    system = 1
    ldap = 2


class ldapSync(BaseModel):
    enable: Optional[bool] = Field(default=False, description="启用同步")
    interval: Optional[int] = Field(default=120, gt=1, description="同步间隔（分钟）")
    default_status: Optional[bool] = Field(default=False, description="是否默认启用")
    sync_rule: Optional[ldapSyncEnum] = Field(default=1, description="冲突时策略 1以平台为主 2以ldap为主")


class ldapSettings(BaseModel):
    config: Optional[ldapConfig] = Field(default=ldapConfig(), description="LDAP连接配置")
    sync: Optional[ldapSync] = Field(default=ldapSync(), description="LDAP同步配置")


class mailServerSettings(BaseModel):
    MAIL_SERVER: Optional[str] = Field(default=None, description="邮件服务器地址")
    MAIL_PORT: Optional[int] = Field(default=None, description="邮件服务器端口")
    MAIL_USERNAME: Optional[str] = Field(default=None, description="邮件服务器用户")
    MAIL_PASSWORD: Optional[str] = Field(default=None, description="邮件服务器密码")
    MAIL_FROM: Optional[str] = Field(default=None, description=" 发件人地址")
    MAIL_FROM_NAME: Optional[str] = Field(default=None, description="邮件标题")
    MAIL_STARTTLS: Optional[bool] = Field(default=True, description="用于 STARTTLS 连接")
    MAIL_SSL_TLS: Optional[bool] = Field(default=False, description="用于 SSL 连接")
    USE_CREDENTIALS: Optional[bool] = Field(default=True, description="否登录到服务器")
    VALIDATE_CERTS: Optional[bool] = Field(default=True, description="是否验证邮件服务器证书")


class channelsSeetings(BaseModel):
    email: Optional[mailServerSettings] = mailServerSettings()


class CheckModeTypeEnum(IntEnum):
    black_list = 1
    white_list = 2


class securitySettings(BaseModel):
    totp: Optional[bool] = Field(default=False, description="开启TOTP")
    ip_check: Optional[bool] = Field(default=False, description="IP地址校验")
    ip_check_mode: CheckModeTypeEnum = Field(default=1, description="IP地址校验模式")
    ip_black_list: Optional[List[str]] = Field(default=[], description="IP黑名单")
    ip_white_list: Optional[List[str]] = Field(default=[], description="IP白名单")


class Setings(BaseModel):
    general: Optional[generalSettings] = Field(default=generalSettings(), description="常规配置")
    ldap: Optional[ldapSettings] = Field(default=ldapSettings(), description="ldap配置")
    security: Optional[securitySettings] = Field(default=securitySettings(), description="安全配置")
    channels: Optional[channelsSeetings] = Field(default=channelsSeetings(), description="通知渠道")


class getSetingsResponse(BaseResponse):
    data: Optional[Setings] = Field(default=None, description="完整配置")
