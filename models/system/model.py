#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：model.py
@Author ：Cary
@Date ：2024/2/26 21:19
@Descripttion : ""
"""
from tortoise import fields, Model

from models.fileds import UnixDateTimeField


class SystemSettings(Model):
    """
    系统设置
    """
    id = fields.BigIntField(pk=True, generated=False, default=1)
    create_at = UnixDateTimeField(is_auto_now_add=True, null=True, description='创建时间')
    update_at = UnixDateTimeField(is_auto_now=True, null=True, description="更新时间")
    general = fields.JSONField(default={}, description="常规配置", null=True)
    security = fields.JSONField(default={}, description="安全设置", null=True)
    channels = fields.JSONField(default={}, description="通知渠道", null=True)

    class Meta:
        table = "sys_settings"
        table_description = "系统设置"
