#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：password_tools.py
@Author ：Cary
@Date ：2024/2/19 00:07
@Descripttion : "安全相关工具"
"""
import base64
import binascii
import hashlib
import uuid
from passlib import pwd
from passlib.context import CryptContext
from jose import jwt
from utils.config import settings
from utils.encryption import AESCBC

# passlib密码加密不可解密为明文
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# aes加密密码可解密为明文
aeshash = AESCBC(settings.SECRET_KEY, settings.SECRET_IV)


def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)


def generate_password(length: int):
    """
    生成随机密码
    """
    return pwd.genword(length=length, charset='ascii_72')


def verify_password(plain_password, hashed_password):
    # passlib验证密码
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # passlib加密密码
    return pwd_context.hash(password)


def aes_hash_password(password):
    """
    AES密码加密
    :param password:
    :return:
    """
    hash_res = aeshash.encrypt(password)
    if hash_res.get("code"):
        return hash_res.get("data")
    raise ValueError("密码加密失败")


def aes_decrypt_password(hash_password):
    """
    AES密码解密
    :param hash_password:
    :return:
    """
    hash_res = aeshash.decrypt(hash_password)
    if hash_res.get("code"):
        return hash_res.get("data")
    raise ValueError("密码解密失败")


def aes_verify_password(password, old_password):
    """
    AES密码校验
    :param password: 输入的密码
    :param old_password: 数据库中的密码
    :return:
    """
    re_password = aes_hash_password(password)
    if re_password == old_password:
        return True
    return False


def is_base64(s):
    try:
        # 将字符串解码为二进制数据
        decoded_data = base64.b64decode(s)
        # 将二进制数据编码为字符串
        encoded_data = base64.b64encode(decoded_data)
        # 检查字符串长度和字符范围
        if len(s) % 4 == 0 and encoded_data == s.encode():
            return True
        else:
            return False
    except Exception:
        return False


def jwt_decode(token, verify_exp=True):
    """
    jwt解密
    :param token:
    :param verify_exp:
    :return:
    """

    # token解密
    payload = jwt.decode(
        token,
        settings.SECRET_JWT_KEY,
        algorithms=[settings.SECRET_JWT_ALGORITHM],
        options={"verify_exp": verify_exp}
    )
    return payload


if __name__ == "__main__":
    test = aes_hash_password("saldja&**^%$56")
    print(test)
    print(is_base64(test))
    print(generate_password(12))
