#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：users_schema.py
@Author ：Cary
@Date ：2024/2/17 21:36
@Descripttion : ""
"""
from pydantic import BaseModel, Field
from models.auth.model import AuthUsers
from schemas.base import BaseResponse
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from typing import Optional, Dict, List


# -------------------------------用户创建---------------------------------
class UserCreateRequest(pydantic_model_creator(
    cls=AuthUsers,
    name="UserCreateRequest",
    exclude_readonly=True,
)):
    """
    单用户创建请求
    """
    roles: Optional[List[int]] = Field(default=None, description="角色列表")


# 单用户返回结果用于序列化
UserCreateResult = pydantic_model_creator(
    cls=AuthUsers,
    name="UserCreateResult",
    exclude=('password',)
)


# 单用户返回结果用于文档
class UserCreateResultDocs(UserCreateResult):
    roles: Optional[List[int]] = Field(default=None, description="角色列表")


class UserCreateResponse(BaseResponse):
    """
    单用户创建响应
    """
    data: Optional[UserCreateResultDocs] = None


# -------------------------------用户删除---------------------------------
class UserDeleteResponse(BaseResponse):
    """
    单用户删除响应
    """
    data: Optional[Dict] = {
        "id": 0
    }


class UserBulkDeleteRequest(BaseModel):
    """
    批量用户删除请求
    """
    user_list: List[int] = Field(description="用户ID列表")


class UserBulkDeleteResponse(BaseResponse):
    """
    批量用户删除响应
    """
    data: Optional[List[int]]


# -------------------------------用户更新---------------------------------
class UserUpdateRequest(pydantic_model_creator(
    cls=AuthUsers,
    name="UserUpdateRequest",
    exclude=("username", "password",),
    exclude_readonly=True,
    optional=("nickname",)
)):
    """
    单用户更新请求
    """
    roles: Optional[List[int]] = Field(default=None, description="角色列表")
    update_roles: bool = Field(default=False, description="是否要更新角色，更新则必须设置为true")


# 单用户更新结果用于序列化
UserUpdateResult = pydantic_model_creator(
    cls=AuthUsers,
    name="UserUpdateResult",
    exclude=('password',)
)


# 单用户更新结果用于文档
class UserUpdateResultDocs(UserUpdateResult):
    roles: Optional[List[int]] = Field(default=None, description="角色列表")


class UserUpdateResponse(BaseResponse):
    """
    单用户更新响应
    """
    data: Optional[UserUpdateResultDocs] = None


class UserBulkUpdateRequest(BaseModel):
    """
    批量用户更新请求
    """
    user_list: List[int] = Field(description="用户ID列表")
    user_type: Optional[int] = Field(default=None, description="用户类型")
    user_status: Optional[bool] = Field(default=None, description="用户状态")
    roles: Optional[List[int]] = Field(default=None, description="角色列表")
    update_roles: bool = Field(default=False, description="是否要更新角色，更新则必须设置为true")


class UserBulkUpdateResponse(BaseResponse):
    """
    批量用户更新响应
    """
    data: Optional[List[int]] = None


# -------------------------------用户查询---------------------------------
# 当前用户查询结果
UserGetResult = pydantic_model_creator(
    cls=AuthUsers,
    name="UserGetResult",
    exclude=('password',)
)


class UserGetResponse(BaseResponse):
    """
    当前用户查询响应
    """
    data: Optional[UserUpdateResult] = None


# 用户过滤结果
UserQuerySet = pydantic_queryset_creator(
    cls=AuthUsers,
    name="UserQuerySet",
    exclude=('password',)
)


# 过滤结果总数和分页
class UserQueryResultsDocs(BaseModel):
    result: Optional[List[UserCreateResultDocs]] = None
    total: Optional[int] = None
    page_total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None


class UserQueryResponse(BaseResponse):
    """
    用户过滤响应
    """
    data: Optional[UserQueryResultsDocs] = None


# -------------------------------修改密码---------------------------------
class UserSetPasswordRequest(BaseModel):
    user_id: int
    is_reset: Optional[bool] = Field(default=False, description="是否重置密码")
    password: str = Field(default=None, description="新密码")
    repassword: str = Field(default=None, description="确认密码")
