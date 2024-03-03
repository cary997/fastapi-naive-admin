#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：settings_api.py
@Author ：Cary
@Date ：2024/2/26 22:37
@Descripttion : ""
"""
from typing import Annotated
from fastapi import APIRouter, Depends

from apis.system.depends import set_settings_depends
from models.system.default_seetings import default_settings
from core.Exeption.Response import success, fail
from schemas.system import settings_schema
from models.system.model import SystemSettings
from utils.cache_tools import redis_exists_key, set_redis_data, get_redis_data

router = APIRouter(prefix='/settings')


@router.get('/get', summary="获取系统配置", response_model=settings_schema.getSetingsResponse)
async def get_settings():
    cache_state = await redis_exists_key("sys:settings")
    if not cache_state:
        data = await SystemSettings.get_or_create(defaults=default_settings, pk=1)
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
