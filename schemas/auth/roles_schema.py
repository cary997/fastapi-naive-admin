#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：roles_schema.py
@Author ：Cary
@Date ：2024/1/24 23:31
@Descripttion : ""
"""
from pydantic import Field, BaseModel

from models.auth.model import AuthRoles
from schemas.base import BaseResponse
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from typing import Optional, List, Dict


# -------------------------------角色创建---------------------------------
class RoleCreateRequest(pydantic_model_creator(
    cls=AuthRoles,
    name="RoleCreateRequest",
    exclude=('roles_users',),
    exclude_readonly=True
)):
    """
    用户组创建请求
    """
    menus: Optional[List[int]] = Field(default=None, description="菜单 id 列表")


RoleCreateResult = pydantic_model_creator(
    cls=AuthRoles,
    exclude=('roles_users',),
    name="RoleCreateResult"
)


class RoleCreateResultDocs(RoleCreateResult):
    menus: Optional[List[int]] = Field(default=None, description="菜单 id 列表")


class RoleCreateResponse(BaseResponse):
    """
    用户组创建响应
    """
    data: Optional[RoleCreateResultDocs] = None


# -------------------------------角色删除---------------------------------
class RoleDeleteResponse(BaseResponse):
    """
    单角色删除响应
    """
    data: Optional[Dict] = {
        "role_id": 1
    }


# -------------------------------角色更新---------------------------------
class RoleUpdateRequest(pydantic_model_creator(
    cls=AuthRoles,
    name="RoleUpdateRequest",
    optional=("name", "nickname"),
    exclude=('roles_users',),
    exclude_readonly=True
)):
    """
    单角色更新请求
    """
    menus: Optional[List[int]] = Field(default=None, description="菜单 id 列表")


# 单用户更新结果
RoleUpdateResult = pydantic_model_creator(
    cls=AuthRoles,
    exclude=('roles_users',),
    name="RoleUpdateResult"
)


class RoleUpdateResultDocs(RoleUpdateResult):
    menus: Optional[List[int]] = Field(default=None, description="菜单 id 列表")


class RoleUpdateResponse(BaseResponse):
    """
    单用户更新响应
    """
    data: Optional[RoleUpdateResultDocs] = None


# -------------------------------角色查询---------------------------------


# 角色列表结果
RoleQuerySet = pydantic_queryset_creator(
    cls=AuthRoles,
    name="RoleQuerySet",
    computed=('user_count',),
)


class RoleQueryResultDocs(BaseModel):
    result: Optional[List[RoleCreateResultDocs]]


class RoleQueryResponse(BaseResponse):
    """
    角色列表响应
    """
    data: Optional[RoleQueryResultDocs] = None
