#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：async_routes_api.py
@Author ：Cary
@Date ：2024/2/20 23:31
@Descripttion : ""
"""
from fastapi import APIRouter, Request, Security
from core.Exeption.Response import fail, success
from core.Security.auth_jwt import check_user_jwt
from models.auth.model import AuthUsers, AuthMenus
from schemas.login.async_routes_schema import MenusTreeResponse
from schemas.auth import users_schema
from utils.config import settings
from utils.serialization_tools import ToTree

router = APIRouter()


@router.get(settings.SYS_ROUTER_SYNCROUTES, summary="同步后端路由菜单", response_model=MenusTreeResponse,
            dependencies=[Security(check_user_jwt)])
async def async_routes(req: Request):
    user_id = req.state.user_id
    get_user = await AuthUsers.get_or_none(pk=user_id)
    if not get_user:
        return fail(message="用户不存在")
    # 判断是否为超级管理员
    is_super = await get_user.roles.filter(pk=1)
    if is_super:
        routers = ToTree(await AuthMenus.all(), True, "meta.rank").list_to_tree()
        return success(message="同步菜单成功", data=routers)

    # 获取user,格式化routers
    user = await users_schema.UserGetResult.from_tortoise_orm(get_user)
    menus_list = []
    menus_id = []
    roles = user.model_dump().get('roles')
    for role in roles:
        if role['role_status'] != False and 'menus' in role:
            for menu in role['menus']:
                if menu['id'] not in menus_id:
                    menus_list.append(menu)
                    menus_id.append(menu['id'])
    routers = ToTree(menus_list, True, "meta.rank").list_to_tree()
    return success(message="同步菜单成功", data=routers)
