#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：model.py
@Author ：Cary
@Date ：2024/1/24 15:06
@Descripttion : ""
"""

from enum import IntEnum
from models.base import BaseModel
from tortoise import fields


class UserTypeEnum(IntEnum):
    local = 1
    ldap = 2


class AuthUsers(BaseModel):
    """
    用户
    """
    username = fields.CharField(max_length=32, unique=True, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    nickname = fields.CharField(max_length=32, description="显示名称")
    phone = fields.CharField(null=True, max_length=20, unique=True, description="手机号")
    email = fields.CharField(null=True, max_length=128, description="邮箱")
    user_type = fields.IntEnumField(enum_type=UserTypeEnum, default=1, description="用户类型(1=local,2=ldap)")
    user_status = fields.BooleanField(default=True, description="True:启用 False:禁用")
    totp = fields.CharField(null=True, max_length=64,description="otp Key")
    roles: fields.ManyToManyRelation['AuthRoles'] = \
        fields.ManyToManyField("models.AuthRoles",
                               related_name="roles_users",
                               on_delete=fields.CASCADE,
                               through="auth_users_roles",
                               forward_key="auth_roles_id",
                               backward_key="auth_users_id"
                               )

    class Meta:
        table = "auth_users"
        table_description = "用户信息"
        indexes = ("username", "user_status")

    class PydanticMeta:
        exclude = ('totp',)


class AuthRoles(BaseModel):
    """
    角色
    """
    name = fields.CharField(max_length=32, unique=True, description="角色标识")
    nickname = fields.CharField(max_length=32, description="角色显示名称")
    desc = fields.CharField(max_length=64, null=True, description="描述")
    role_status = fields.BooleanField(default=True, description="True:启用 False:禁用")
    menus: fields.ManyToManyRelation['AuthMenus'] = \
        fields.ManyToManyField("models.AuthMenus",
                               related_name="menus_roles",
                               on_delete=fields.CASCADE,
                               through="auth_roles_menus",
                               forward_key="auth_menus_id",
                               backward_key="auth_roles_id"
                               )
    users: fields.ManyToManyRelation['AuthUsers']

    # 计算关联用户数
    def user_count(self) -> int:
        return len(self.roles_users)

    class Meta:
        table = "auth_roles"
        table_description = "角色信息"
        indexes = ("name",)


class AuthMenus(BaseModel):
    """
    菜单
    """
    path = fields.CharField(max_length=512, unique=True, description="url")
    name = fields.CharField(max_length=512, unique=True, description="唯一标识或外链链接")
    redirect = fields.CharField(max_length=512, description="重定向url", null=True)
    component = fields.CharField(max_length=512, description="组件路径", null=True)
    meta = fields.JSONField(default={}, description="菜单元数据", null=True)
    parent = fields.BigIntField(default=None, description="上级菜单", null=True)
    roles: fields.ManyToManyRelation['AuthRoles']

    class Meta:
        table = "auth_menus"
        table_description = "菜单信息"
        indexes = ("name",)

    class PydanticMeta:
        exclude = ('menus_roles',)
