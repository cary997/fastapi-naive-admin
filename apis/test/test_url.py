#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastcow-server
@File ：test_url.py
@Author ：Cary
@Date ：2024/3/3 8:22
@Descripttion : ""
"""
from fastapi import APIRouter
from apis.test import test

testRouters = APIRouter()
testRouters.include_router(test.router)
