#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：async_routes_schema.py
@Author ：Cary
@Date ：2024/2/20 23:32
@Descripttion : ""
"""
from typing import Optional, List

from tortoise.contrib.pydantic import pydantic_model_creator

from schemas.base import BaseResponse
from schemas.auth.menus_schema import MenuMeta

from models.auth.model import AuthMenus


class Menus(pydantic_model_creator(
    cls=AuthMenus,
    name="MenuCreateRequest",
)):
    meta: MenuMeta


class MenusTree(Menus):
    parent_key: Optional[str]
    children: Optional[List[Menus]]


class MenusTreeResponse(BaseResponse):
    data: List[MenusTree]
