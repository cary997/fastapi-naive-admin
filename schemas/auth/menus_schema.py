#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：menus_schema.py
@Author ：Cary
@Date ：2024/1/24 23:31
@Descripttion : ""
"""
from enum import IntEnum
from pydantic import BaseModel, Field
from models.auth.model import AuthMenus
from schemas.base import BaseResponse
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from typing import Optional, Dict, List


class MenusTypeEnum(IntEnum):
    directory = 1
    pages = 2
    button = 3
    extlink = 4


class MenuMeta(BaseModel):
    title: str = Field(description="中文标题")
    en_title: str = Field(description="英文标题")
    menu_type: MenusTypeEnum = Field(description="菜单类型(directory=1,pages=2,button=3,extlink=4")
    icon: Optional[str] = Field(default=None, description="图标")
    showLink: Optional[bool] = Field(default=True, description="是否在菜单中显示")
    showParent: Optional[bool] = Field(default=True, description="是否显示父级菜单")
    keepAlive: Optional[bool] = Field(default=False, description="是否缓存页面")
    frameSrc: Optional[str] = Field(default=None, description="内嵌的iframe链接")
    frameLoading: Optional[bool] = Field(default=True, description="是否开启首次加载动画")
    hiddenTag: Optional[bool] = Field(default=False, description="是否在标签页隐藏")
    enterTransition: Optional[str] = Field(default=None, description="页面进入动画")
    leaveTransition: Optional[str] = Field(default=None, description="页面离开动画")
    rank: Optional[int] = Field(default=None, description="菜单排序针对directory类型生效")


# -------------------------------菜单创建---------------------------------
class MenuCreateRequest(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuCreateRequest",
    exclude_readonly=True
)):
    """
    菜单创建请求
    """
    meta: MenuMeta


class MenuCreateResult(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuCreateResult"
)):
    meta: MenuMeta


class MenuCreateResponse(BaseResponse):
    """
    菜单创建响应
    """
    data: Optional[MenuCreateResult] = None


# -------------------------------菜单删除---------------------------------
class MenuDeleteResponse(BaseResponse):
    """
    菜单删除响应
    """
    data: Optional[Dict] = {
        "menu_id": 1
    }


# -------------------------------菜单更新---------------------------------
class MenuUpdateRequest(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuUpdateRequest",
    exclude_readonly=True,
    optional=("path", "name", "meta",)
)):
    """
    菜单更新请求
    """
    meta: Optional[MenuMeta] = None


# 菜单更新结果
class MenuUpdateResult(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuUpdateResult"
)):
    meta: MenuMeta


class MenuUpdateResponse(BaseResponse):
    """
    菜单更新响应
    """
    data: Optional[MenuUpdateResult] = None


# -------------------------------菜单查询---------------------------------
# 菜单查询结果
class MenuGetResult(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuGetResult"
)):
    meta: MenuMeta


class MenuGetResponse(BaseResponse):
    """
    菜单查询响应
    """
    data: Optional[MenuGetResult] = None


# 菜单树形结构
class MenuTreeResult(MenuGetResult):
    children: Optional[List[MenuGetResult]] = None


class MenuQueryResults(BaseModel):
    result: Optional[List[MenuTreeResult]] = None


class MenuQueryResponse(BaseResponse):
    """
    菜单过滤响应
    """
    data: Optional[MenuQueryResults] = None
