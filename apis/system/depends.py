#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：depends.py
@Author ：Cary
@Date ：2024/3/3 6:23
@Descripttion : ""
"""
from core.Exeption.Response import fail
from schemas.system import settings_schema
from utils.ipaddress_tools import check_ip_list
from utils.password_tools import aes_hash_password, is_base64


async def set_settings_depends(update_content: settings_schema.Setings):
    # 检查安全配置中的IP黑白名单中的IP是否符合规范
    ip_list = []
    update_dict = update_content.dict(exclude_unset=True, exclude_none=True)
    if 'security' in update_dict:
        ip_white_list = update_dict.get('security').get('ip_white_list')
        ip_black_list = update_dict.get('security').get('ip_black_list')
        if bool(ip_white_list) or bool(ip_black_list):
            ip_list = [*ip_white_list, *ip_black_list]
    if bool(ip_list):
        check_state, failed_ip = await check_ip_list(ip_list)
        if not check_state:
            return fail(message=f"请检查IP或IP范围格式 {failed_ip}")

    # 配置中的密码加密
    if 'channels' in update_dict:
        channels = update_dict.get('channels')
        mail_password = channels.get('email').get('MAIL_PASSWORD')
        if mail_password is not None and not is_base64(mail_password):
            update_dict['channels']['email']['MAIL_PASSWORD'] = aes_hash_password(
                mail_password)
    return update_dict
