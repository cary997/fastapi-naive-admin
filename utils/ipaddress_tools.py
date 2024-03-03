#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：ipaddress_tools.py
@Author ：Cary
@Date ：2024/3/2 3:31
@Descripttion : ""
"""
import ipaddress
from typing import List

from IPy import IP


def is_ip(ip: str) -> bool:
    """
    判断是否是IP地址支持IPV4 IPV6 IP地址 IP地址/掩码 IP地址-IP地址
    """
    try:
        IP(ip)
        return True
    except ValueError:
        return False


def ip_range_to_tuple(ip_range: str, divide: str = '-') -> (str, str):
    """
    ip_range : 192.168.1.0-192.168.1.255
    return: 起始IP和结束IP
    """
    try:
        start, end = ip_range.split(divide)
        return start, end
    except ValueError:
        return None, None


def is_ip_in_range(ip, ip_range, divide: str = '-'):
    """
    判断IP是否在'192.168.1.1-192.168.1.255'类型的范围里
    """
    start_ip, end_ip = ip_range_to_tuple(ip_range, divide)
    if is_ip(start_ip) and is_ip(end_ip) and is_ip(ip):
        start_ip = IP(start_ip)
        end_ip = IP(end_ip)
        ip = IP(ip)
        return True if start_ip <= ip <= end_ip else False
    else:
        return False


async def check_ip_list(ip_list: List[str], divide: str = '-') -> (bool, str):
    """
    检查IP列表中的IP是否全部符合规范
    ip_list : ['192.168.1.1', '192.168.1.2']
    divide : '-'
    """
    check_state = True
    failed_ip = None
    for ip in ip_list:
        if not is_ip(ip):
            if not ip.__contains__(divide):
                check_state = False
                failed_ip = ip
                break
            else:
                start_ip, end_ip = ip_range_to_tuple(ip)
                if not is_ip(start_ip) or not is_ip(end_ip):
                    check_state = False
                    failed_ip = ip
                    break
                if IP(start_ip) >= IP(end_ip):
                    check_state = False
                    failed_ip = ip
                    break
    return check_state, failed_ip


if __name__ == '__main__':
    a = is_ip_in_range('192.168.1.1', '192.168.1.1-192.168.1.255')
    print(a)
