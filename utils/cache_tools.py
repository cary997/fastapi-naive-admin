#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：cache_tools.py
@Author ：Cary
@Date ：2024/3/1 0:54
@Descripttion : ""
"""
import asyncio
import json
from builtins import anext
from extend.redis.init import get_redis
from utils.serialization_tools import get_dict_target_value


def is_json(data):
    """
    判断是否为json
    """
    try:
        if data is None:
            return False
        json.loads(data)
    except ValueError:
        return False
    return True


async def redis_exists_key(key: str):
    """
    key : reids中的key
    判断key是否存在，数据为空也视为不存在
    """
    _c = get_redis()
    cache = await anext(_c)
    try:
        # 返回值1和0
        state = await cache.exists(key)
        if not state:
            return False
        data = await cache.get(key)
        if not data:
            return False
        return True
    except Exception as e:
        return False


async def get_redis_data(key: str, value_key: str = None):
    """
    key : reids中的key
    value_key : 如果是个json可直接查找json里的字段
    """
    _c = get_redis()
    cache = await anext(_c)
    try:
        is_empty = await redis_exists_key(key)
        if not is_empty:
            return None
        data = await cache.get(key)
        if is_json(data):
            data = json.loads(data)
            if value_key:
                return get_dict_target_value(data, value_key)
        return data
    except Exception as e:
        raise e


async def set_redis_data(key: str, value=None, **kwargs):
    """
    key : reids中的key
    value : 要存的数据
    """
    _c = get_redis()
    cache = await anext(_c)
    try:
        if isinstance(value, dict):
            value = json.dumps(value)
        await cache.set(key, value, **kwargs)
    except Exception as e:
        raise e


if __name__ == '__main__':
    asyncio.run(get_redis_data('sys:settings', 'channels.email'))
    # asyncio.run(set_redis_data('k1', {'a': 1, 'b': 2}, ex=200))
    # asyncio.run(redis_exists_key('sys:settings'))
