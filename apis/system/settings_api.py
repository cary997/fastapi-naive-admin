#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：settings_api.py
@Author ：Cary
@Date ：2024/2/26 22:37
@Descripttion : ""
"""
from typing import Annotated
from fastapi import APIRouter, Depends

from apis.system.depends import set_settings_depends
from extend.ldap.auth_mixin import LdapAuthMixin
from models.auth.model import AuthUsers, AuthRoles
from core.Exeption.Response import success, fail
from schemas.system import settings_schema
from models.system.model import SystemSettings
from schemas.system.settings_schema import Setings, ldapSettings
from utils.cache_tools import redis_exists_key, set_redis_data, get_redis_data
from utils.password_tools import generate_password

router = APIRouter(prefix='/settings')


@router.get('/get', summary="获取系统配置", response_model=settings_schema.getSetingsResponse)
async def get_settings():
    cache_state = await redis_exists_key("sys:settings")
    if not cache_state:
        data = await SystemSettings.get_or_create(defaults=Setings().model_dump(), pk=1)
        format_data = await settings_schema.SystemSettingsResult.from_tortoise_orm(data[0])
        await set_redis_data("sys:settings", value=format_data.model_dump())
    else:
        format_data = await get_redis_data("sys:settings")
    return success(message="查询成功", data=format_data)


@router.patch('/set', summary="更新系统配置", response_model=settings_schema.getSetingsResponse)
async def set_settings(update_content: Annotated[dict, Depends(set_settings_depends)]):
    # 判断配置是否存在
    sys_settings = await SystemSettings.get_or_none(pk=1)
    if not sys_settings:
        return fail(message="对象不存在")
    # 更新并缓存
    update_settings = await sys_settings.update_from_dict(update_content)
    await update_settings.save()
    format_data = await settings_schema.SystemSettingsResult.from_tortoise_orm(update_settings)
    await set_redis_data("sys:settings", value=format_data.model_dump())
    return success(message="更新成功", data=format_data)


@router.post('/syncldap', summary="ldap同步")
async def syncldap(settings: ldapSettings):
    settings = settings.model_dump()
    _config = settings.get('config')
    _sync = settings.get('sync')
    conn = LdapAuthMixin(**_config)
    _res = conn.search_user(is_all=True)
    if not _res.get('code'):
        return fail(message=f"{_res.get('message')}", data=_res.get('data'))
    data = _res.get('data')
    attributes = _config.get('attributes')
    _user_list = []
    for _user in data:
        _data = _user.get('attributes')
        _emial = _data.get(attributes.get('email'))
        _phone = _data.get(attributes.get('phone'))
        user_to_db = AuthUsers(username=_data.get(attributes.get('username'))[0],
                               nickname=_data.get(attributes.get('nickname'))[0],
                               password=generate_password(12),
                               email=_emial[0] if _emial else None,
                               phone=_phone[0] if _phone else None,
                               user_type=2,
                               user_status=True if _sync.get('default_status') else False,
                               )
        _user_list.append(user_to_db)
    if _sync.get('sync_rule') == 1:
        update_fields = ['nickname', 'email', 'phone']
    else:
        update_fields = ['nickname', 'email', 'phone', 'user_type']
    try:
        await AuthUsers.bulk_create(_user_list, on_conflict=['username'], update_fields=update_fields)
        return success(message="同步成功")
    except Exception as e:
        return fail(message=f"同步失败 {e}")
