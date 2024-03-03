#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：base.py
@Author ：Cary
@Date ：2024/2/9 10:47
@Descripttion : "基础model"
"""

from tortoise.models import Model
from tortoise import fields
from models.fileds import UnixDateTimeField


class BaseModel(Model):
    """
    基础抽象基类，包含公共字段
    UnixDateTimeField:自定义时间字段返回int类型的时间戳格式
    """
    id = fields.BigIntField(pk=True)
    create_at = UnixDateTimeField(is_auto_now_add=True, null=True, description='创建时间')
    update_at = UnixDateTimeField(is_auto_now=True, null=True, description="更新时间")

    class Meta:
        abstract = True
