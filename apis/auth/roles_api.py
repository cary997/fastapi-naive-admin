#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：roles_api.py
@Author ：Cary
@Date ：2024/2/8 16:36
@Descripttion : ""
"""

from fastapi import APIRouter
from core.Exeption.Response import fail, success
from schemas.auth import roles_schema
from models.auth.model import AuthRoles, AuthMenus

router = APIRouter(prefix='/roles')


@router.post('/add', summary="创建角色", response_model=roles_schema.RoleCreateResponse)
async def auth_roles_add(create_content: roles_schema.RoleCreateRequest):
    """
    创建角色
    :param create_content:
    :return:
    """
    # 判断角色是否存在
    get_role = await AuthRoles.get_or_none(name=create_content.name)
    if get_role:
        return fail(message=f"对象 {create_content.name} 已经存在!")
    # 创建角色
    add_role = await AuthRoles.create(**create_content.dict(exclude={'menus'}))
    if not add_role:
        return fail(message="创建失败!")
    # 获取menus id列表
    menus = create_content.menus
    # 创建关联菜单
    if menus:
        await add_role.menus.clear()
        menus_list = await AuthMenus.filter(id__in=menus)
        await add_role.menus.add(*menus_list)
    # 序列化返回结果
    form_add_role = await roles_schema.RoleUpdateResult.from_tortoise_orm(add_role)
    result = form_add_role.model_dump()
    result['menus'] = menus
    return success(message="创建成功!", data=result)


@router.delete('/del/{role_id}', summary="删除角色", response_model=roles_schema.RoleDeleteResponse)
async def auth_roles_del(role_id: int):
    """
    删除角色
    :param role_id:
    :return:
    """
    if role_id == 1:
        return fail(message="不能删除平台内置角色！")
    delete_action = await AuthRoles.filter(pk=role_id).delete()
    if not delete_action:
        return fail(message="删除失败", data={"id": role_id})
    return success(message="删除成功", data={"id": role_id})


@router.patch('/set/{role_id}', summary="更新角色", response_model=roles_schema.RoleUpdateResponse)
async def auth_roles_set(role_id: int, update_content: roles_schema.RoleUpdateRequest):
    """
    更新角色
    :param role_id:
    :param update_content:
    :return:
    """
    # 判断角色是否存在
    get_role = await AuthRoles.get_or_none(pk=role_id)
    if not get_role:
        return fail(message="对象不存在")

    # 获取menus id列表
    menus = update_content.menus

    # 更新角色
    update_role = await get_role.update_from_dict(update_content.dict(exclude_unset=True, exclude={'menus'}))
    await update_role.save()

    # 先将菜单情空
    await update_role.menus.clear()
    # 更新关联菜单
    if menus:
        menus_list = await AuthMenus.filter(id__in=menus)
        await update_role.menus.add(*menus_list)
    # 序列化
    form_update_role = await roles_schema.RoleUpdateResult.from_tortoise_orm(update_role)
    result = form_update_role.model_dump()
    result['menus'] = menus
    return success(message=f'更新成功', data=result)


@router.get('/list', summary="角色列表", response_model=roles_schema.RoleQueryResponse)
async def auth_roles_list():
    """
    角色列表
    """

    # 查询结果
    query_data = AuthRoles.all().order_by("name")

    # 序列化查询结果
    form_query_data = await roles_schema.RoleQuerySet.from_queryset(query_data)

    # 过滤菜单使role[menus]中只包含关联菜单的id
    result = []
    for role in form_query_data.model_dump():
        if role.get('menus'):
            role['menus'] = [menus['id'] for menus in role['menus']]
        result.append(role)

    data = {
        "result": result,
    }
    return success(message=f"查询成功", data=data)
