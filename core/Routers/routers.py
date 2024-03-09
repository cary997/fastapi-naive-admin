# !/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@File ：routers.py
@Author ：Cary
@Date ：2024/2/3 16:17
@Descripttion : "路由总入口"
"""
from fastapi import APIRouter, Security, Depends

from apis.test.test_url import testRouters
from core.Security.auth_jwt import check_user_jwt
from utils.config import settings
from core.Routers.cusotm_route import CusotmRoute
from apis.login.login_urls import loginRouters
from apis.auth.auth_urls import authRouters
from apis.system.system_url import systemRouters

Routers = APIRouter(prefix=settings.SYS_ROUTER_PREFIX, route_class=CusotmRoute, )

# 登录
Routers.include_router(loginRouters, tags=["login"])
# 权限
Routers.include_router(authRouters, prefix="/auth", dependencies=[Security(check_user_jwt)], tags=["auth"])
# 系统
Routers.include_router(systemRouters, prefix="/system", dependencies=[Security(check_user_jwt)], tags=["system"])

# 供前端测试接口
Routers.include_router(testRouters, prefix="/test", dependencies=[Security(check_user_jwt)], tags=["test"])
