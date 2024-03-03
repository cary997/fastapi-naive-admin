#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：auth_totp.py
@Author ：Cary
@Date ：2024/2/27 17:44
@Descripttion : ""
"""
import pyotp

from utils.config import settings


def generate_totp(name: str, issuer_name: str = settings.SYS_TITLE) -> dict:
    key = pyotp.random_base32()
    data = pyotp.totp.TOTP(key).provisioning_uri(name=name, issuer_name=issuer_name)
    return {'key': key, 'data': data}


def verify_totp(key: str, token: str) -> bool:
    totp = pyotp.TOTP(key)
    return totp.verify(token)
