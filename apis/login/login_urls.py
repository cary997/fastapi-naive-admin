#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：login_urls.py
@Author ：Cary
@Date ：2024/2/27 20:10
@Descripttion : ""
"""
from fastapi import APIRouter
from apis.login import login_api, async_routes_api

loginRouters = APIRouter()
loginRouters.include_router(login_api.router)
loginRouters.include_router(async_routes_api.router)
