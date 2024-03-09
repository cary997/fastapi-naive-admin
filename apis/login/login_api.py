# !/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：login_schema.py
@Author ：Cary
@Date ：2024/2/20 23:31
@Descripttion : ""
"""
from core.Security.auth_totp import generate_totp, verify_totp
from extend.ldap.auth_mixin import LdapAuthMixin
from models.system.model import SystemSettings
from utils.cache_tools import redis_exists_key, get_redis_data, set_redis_data
from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from pydantic import ValidationError
from core.Security.auth_jwt import issuance_of_jwt
from models.auth.model import AuthUsers
from schemas.login import login_schema
from core.Exeption.Response import fail, success
from utils.password_tools import verify_password, jwt_decode, aes_hash_password, aes_decrypt_password
from utils.config import settings

router = APIRouter()


@router.post(settings.SYS_ROUTER_AUTH2, response_model=login_schema.AccessResponse, response_model_exclude_unset=True,
             summary="用户登录")
async def access_token(post: login_schema.LoginRequestForm = Depends()):


    """
    用户登陆
    :param post:
    :return: jwt token
    """
    # 账号密码验证
    get_user = await AuthUsers.get_or_none(username=post.username)
    if not get_user:
        return fail(message="用户不存在!")
    if not get_user.password:
        return fail(message="用户密码验证失败!")
    if not get_user.user_status:
        return fail(http_code=403, message="用户已被禁用!")
    if get_user.user_type == 1:
        if not verify_password(post.password, get_user.password):
            return fail(message="用户密码不正确!")

    # 判断redis是否缓存了系统配置
    settings_state = await redis_exists_key("sys:settings")
    # 获取系统配置
    if settings_state:
        sys_conf = await get_redis_data("sys:settings")
    else:
        sys_conf = await SystemSettings.get_or_none(pk=1).values()
    # ldap验证
    if get_user.user_type == 2 and sys_conf is not None:
        # 获取ldap配置
        ldap_conf = sys_conf['ldap']['config']
        if not ldap_conf.get('enable'):
            return fail(message="管理员未开启LDAP登录")
        ldap_conn = LdapAuthMixin(**ldap_conf)
        search_res = ldap_conn.search_user(username=post.username)
        _code = search_res.get('code')
        search_data = search_res.get('data')
        if _code and len(search_data) == 0:
            return fail(message="未查询到LDAP用户")
        if not search_res.get('code'):
            return fail(message=f"{search_res.get('message')}")
        verify_user = ldap_conn.verify_user(user=search_data[0].get('dn'), password=post.password)
        if not verify_user.get('code'):
            return fail(message=f"{verify_user.get('message')}")
    # 判断是否开启totp验证
    if sys_conf is not None:
        security_conf = sys_conf['security']
        _totp = security_conf.get('totp')
        # 如果开启了Totp但是没有传对应的code则告诉前端需要重新请求
        if _totp and post.totp_code is None:
            if not get_user.totp:
                new_totp = generate_totp(get_user.username)
                get_user.totp = aes_hash_password(new_totp.get('key'))
                await get_user.save()
                return success(data={"totp": _totp, "new": True, "new_totp": new_totp.get('data')})
            return success(data={"totp": _totp, "new": False, "new_totp": None})
        # 如果开启了Totp也传了code则验证totp
        if _totp and post.totp_code is not None:
            user_totp = aes_decrypt_password(get_user.totp)
            if not verify_totp(user_totp, post.totp_code):
                return fail(message="MFA验证失败!")
    # 如果totp没开启则直接返回token
    # jwt签发成功写入redis
    user_jwt = issuance_of_jwt(get_user)
    await set_redis_data(f"jwt:{get_user.pk}", value=user_jwt.get('access_token'), ex=settings.SECRET_JWT_EXP * 60)
    return success(message="登录成功", data=user_jwt, access_token=user_jwt['access_token'],
                   token_type=user_jwt['token_type'])


@router.post(settings.SYS_ROUTER_REFRESH, response_model=login_schema.RefreshResponse,
             response_model_exclude_unset=True,
             summary="令牌刷新")
async def refresh_token(post: login_schema.RefreshToken):
    """
    刷新jwt
    :param post:
    :return: jwt token
    """
    jwt_validation_error = HTTPException(status_code=401,
                                         headers={"WWW-Authenticate": f"Bearer {post.refresh_token}"}, detail="无效凭证!")
    jwt_expires_error = HTTPException(status_code=401,
                                      headers={"WWW-Authenticate": f"Bearer {post.refresh_token}"}, detail="凭证已过期!")

    try:
        access_payload = jwt_decode(post.access_token, verify_exp=False)
        ref_payload = jwt_decode(post.refresh_token)

        if verify_password(
                f"{access_payload.get('user_id')}{access_payload.get('jid')}{access_payload.get('username')}",
                ref_payload.get('refresh_key')):
            get_user = await AuthUsers.get_or_none(pk=access_payload.get('user_id'))
            if not get_user:
                return fail(http_code=403, message="用户不存在或已删除!")
            if not get_user.user_status:
                return fail(http_code=403, message="用户已被禁用!")
            user_jwt = issuance_of_jwt(get_user)
            # jwt签发成功写入redis
            await set_redis_data(f"jwt:{get_user.pk}", value=user_jwt.get('access_token'),
                                 ex=settings.SECRET_JWT_EXP * 60)
            return success(message="刷新成功", data=user_jwt)
        return jwt_validation_error
    except jwt.ExpiredSignatureError:
        raise jwt_expires_error
    except (JWTError, ValidationError):
        raise jwt_validation_error
