#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：__init__.py
@Author ：Cary
@Date ：2024/2/12 04:27
@Descripttion : ""
"""
from tortoise import Tortoise
from models.auth.model import AuthUsers, AuthRoles, AuthMenus
from models.system.model import SystemSettings

Tortoise.init_models(["models"], "models")
