#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：roles_api.py
@Author ：Cary
@Date ：2024/2/8 16:36
@Descripttion : ""
"""
from fastapi import APIRouter, Query
from core.Exeption.Response import fail, success
from schemas.auth import menus_schema
from models.auth.model import AuthMenus
from utils.serialization_tools import ToTree

router = APIRouter(prefix='/menus')


@router.post('/add', summary="创建菜单", response_model=menus_schema.MenuCreateResponse)
async def auth_menus_add(create_content: menus_schema.MenuCreateRequest):
    """
    创建菜单
    :param create_content:
    :return:
    """
    # 判断菜单是否存在
    get_menu = await AuthMenus.get_or_none(name=create_content.name)
    if get_menu:
        return fail(message=f"对象 {create_content.name} 已存在")

    # 创建菜单
    add_menu = await AuthMenus.create(**create_content.model_dump())
    if not add_menu:
        return fail(message="创建失败")
    # 序列化返回结果
    result = await menus_schema.MenuCreateResult.from_tortoise_orm(add_menu)
    return success(message="创建成功", data=result)


@router.delete('/del/{menu_id}', summary="删除菜单", response_model=menus_schema.MenuDeleteResponse)
async def auth_menus_del(menu_id: int):
    """
    删除菜单
    :param menu_id:
    :return:
    """
    delete_action = await AuthMenus.filter(pk=menu_id).delete()
    if not delete_action:
        return fail(message="删除失败", data={"id": menu_id})
    return success(message="删除成功", data={"id": menu_id})


@router.patch('/set/{menu_id}', summary="更新菜单", response_model=menus_schema.MenuUpdateResponse)
async def auth_menus_set(menu_id: int, update_content: menus_schema.MenuUpdateRequest):
    """
    更新菜单
    :param menu_id:
    :param update_content:
    :return:
    """
    # 判断菜单是否存在
    get_menu = await AuthMenus.get_or_none(pk=menu_id)
    if not get_menu:
        return fail(message="对象不存在")

    # 更新菜单
    update_menu = await get_menu.update_from_dict(update_content.dict(exclude_unset=True))
    await update_menu.save()
    # 序列化
    result = await menus_schema.MenuUpdateResult.from_tortoise_orm(update_menu)
    return success(message="更新成功", data=result)


@router.get('/list', summary="菜单列表", response_model=menus_schema.MenuQueryResponse)
async def auth_menus_list(
        to_tree: bool = Query(True)
):
    """
    过滤菜单
    """

    # 查询结果
    query_data = await AuthMenus.all()

    # 格式化为树
    if to_tree:
        query_data = ToTree(query_data, True, "meta.rank").list_to_tree()

    # 序列化查询结果
    data = {
        "result": query_data
    }
    return success(message="查询成功", data=data)
