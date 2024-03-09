#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：auth_jwt.py
@Author ：Cary
@Date ：2024/2/18 20:38
@Descripttion : "JWT生成"
"""
import time
from datetime import datetime, timedelta
from typing import Dict
from jose import JWTError, jwt
from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from extend.redis.init import redisCache
from models.auth.model import AuthUsers
from utils.config import settings
from utils.password_tools import jwt_decode, get_password_hash, random_str

# openssl rand -hex 32
SECRET_KEY = settings.SECRET_JWT_KEY
ALGORITHM = settings.SECRET_JWT_ALGORITHM
OAuth2 = OAuth2PasswordBearer(tokenUrl=f'{settings.SYS_ROUTER_PREFIX}{settings.SYS_ROUTER_AUTH2}')


def create_token(subject: Dict, exp: int) -> str:
    """
    生成token
    :param exp:
    :param subject:需要存储到token的数据
    :return:
    """
    expires = int(time.mktime((datetime.now() + timedelta(minutes=exp)).timetuple()))
    subject.update(exp=expires)
    encoded_jwt = jwt.encode(subject, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


ACCESS_TOKEN_EXPIRE_MINUTES = settings.SECRET_JWT_EXP
REFRESH_TOKEN_EXPIRE_MINUTES = settings.SECRET_REJWT_EXP


def issuance_of_jwt(user: AuthUsers):
    """
    签发jwt
    :param user:
    :return:
    """
    jid = get_password_hash(random_str())
    username = user.username
    nickname = user.nickname
    user_id = user.pk

    jwt_data = {
        "username": username,
        "user_id": user_id,
        "jid": jid
    }
    access_token = create_token(subject=jwt_data, exp=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(subject={
        "refresh_key": get_password_hash(f"{user_id}{jid}{username}")
    }, exp=REFRESH_TOKEN_EXPIRE_MINUTES)

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": int(time.mktime((datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timetuple())),
        "token_type": "Bearer",
        "user_id": user_id,
        "username": username,
        "nickname": nickname,
    }
    return data


async def check_user_jwt(req: Request,  token: str = Depends(OAuth2)):
    """
    权限验证
    :param token:
    :param req:
    :return:
    """
    jwt_validation_error = HTTPException(status_code=401,
                                         headers={"WWW-Authenticate": f"Bearer {token}"}, detail="无效凭证!")
    jwt_expires_error = HTTPException(status_code=401,
                                      headers={"WWW-Authenticate": f"Bearer {token}"}, detail="凭证已过期!")
    try:
        # token解密
        payload = jwt_decode(token)
        if payload:
            # 用户ID
            user_id = payload.get("user_id", None)
            # 用户名
            username = payload.get("username", None)
            # 无效用户信息
            if user_id is None or username is None:
                raise jwt_validation_error
            # 查询redis是否存在jwt
            cache: redisCache = req.app.state.cache
            cache_token = await cache.get(f"jwt:{user_id}")
            # 如果和reids中的key不一致则前端请求刷新
            if cache_token != token:
                raise jwt_expires_error
        else:
            raise jwt_validation_error

    except jwt.ExpiredSignatureError:
        raise jwt_expires_error
    except (JWTError, ValidationError):
        raise jwt_validation_error

    # ---------------------------------------验证权限-------------------------------------------------------------------
    # 缓存用户ID至request
    req.state.user_id = user_id
    # # 缓存用户名
    # req.state.username = username
