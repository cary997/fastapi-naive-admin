#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：system_url.py
@Author ：Cary
@Date ：2024/2/26 22:37
@Descripttion : ""
"""
from fastapi import APIRouter
from apis.system import settings_api

systemRouters = APIRouter()
systemRouters.include_router(settings_api.router)
