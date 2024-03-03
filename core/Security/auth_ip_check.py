#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：auth_ip_check.py
@Author ：Cary
@Date ：2024/3/1 2:36
@Descripttion : ""
"""
from fastapi import Request
from IPy import IP
from utils.cache_tools import redis_exists_key, get_redis_data
from utils.ipaddress_tools import is_ip, is_ip_in_range


async def get_client_ip(request: Request) -> str:
    """
    按照优先级获取request请求头中的客户端IP
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if isinstance(x_forwarded_for, list) and x_forwarded_for:
        return x_forwarded_for[0]
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    elif request.headers.get('X-Forwarded-Host'):
        return request.headers.get('X-Forwarded-Host')
    else:
        return request.client.host


async def verify_client_ip(client_ip: str) -> bool:
    """
    校验客户端IP是否运行访问
    """
    # 读取redis系统配置
    state = await redis_exists_key('sys:settings')
    if not state:
        return True
    # 读取redis系统配置中的安全设置
    security_settings = await get_redis_data('sys:settings', 'security')
    # 判断是否开启了IP地址检查
    if not security_settings.get('ip_check'):
        return True
    # 根据IP地址检查模式获取不同模式的IP列表
    mode = security_settings.get('ip_check_mode')
    if mode == 1:
        ip_list = security_settings.get('ip_black_list')
    else:
        ip_list = security_settings.get('ip_white_list')
    if len(ip_list) == 0:
        return True
    # 判断client_ip 是否符合要求
    _ip_state = None
    for ip in ip_list:
        if is_ip(ip):
            if client_ip in IP(ip):
                _ip_state = False if mode == 1 else True
                break
            else:
                _ip_state = True if mode == 1 else False
        else:
            if ip.__contains__("-") and is_ip_in_range(client_ip, ip):
                _ip_state = False if mode == 1 else True
                break
            else:
                _ip_state = False
    return _ip_state
