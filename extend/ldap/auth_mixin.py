#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：auth_mixin.py
@Author ：Cary
@Date ：2024/3/4 17:41
@Descripttion : ""
"""
from typing import List

from ldap3 import Server, ServerPool, Connection, ASYNC
from ldap3.core.exceptions import LDAPInvalidCredentialsResult
from loguru import logger
from pydantic import BaseModel, Field

from utils.password_tools import is_decrypt, aes_decrypt_password


class attributesMap(BaseModel):
    username: str = Field(default="sAMAccountName", description="username映射字段")
    nickname: str = Field(default="cn", description="nickname映射字段")
    email: str = Field(default="mail", description="email映射字段")
    phone: str = Field(default="telephoneNumber", description="phone映射字段")


def ldap_res(code: int = 1, message=None, data=None):
    return {'code': code, 'message': message, 'data': data}


class LdapAuthMixin(object):
    def __init__(self, hosts: List[str], user: str, password: str, base_ou: str,
                 attributes: attributesMap = attributesMap(), paged_size: int = 500, **kwargs):
        """
        初始化ldap连接池
        :param hosts: 主机列表["ldap(s)://ldap.dc01.com:389","ldap(s)://ldap.dc02.com:389"]
        :param user: 绑定用户 CN=test,CN=Users,DC=example,DC=com
        :param password: 绑定密码
        :param base_ou: 搜寻用户的基础OU OU=base,DC=example,DC=com
        :param attributes: 字段映射关系 attributesMap
        """
        """初始化ldap连接池"""
        self.base_ou = base_ou
        self.attributes = attributes
        self.paged_size = paged_size
        conn_pool = ServerPool(None, pool_strategy='ROUND_ROBIN', active=2, exhaust=True)
        try:
            if not isinstance(hosts, List):
                hosts = [hosts]
            for host in hosts:
                conn_pool.add(Server(host=host, get_info=None))
            if is_decrypt(password):
                password = aes_decrypt_password(password)
            self.conn = Connection(conn_pool, user=user, password=password, auto_bind=True, )
            self.conn_bind = True
            self.conn_messagr = None
        except Exception as e:
            self.conn_bind = False
            self.conn_messagr = e

    def search_user(self, username: str = None, is_all: bool = False):
        """根据username搜索user或is_all搜索全部user"""
        if username is None and is_all is False:
            return ldap_res(code=0, message="缺少参数", data=[])
        if not self.conn_bind:
            logger.error(self.conn_messagr)
            return ldap_res(code=0, message=self.conn_messagr, data=[])
        try:
            _attributes = []
            if not isinstance(self.attributes, dict):
                self.attributes = self.attributes.model_dump()
            for key, value in self.attributes.items():
                _attributes.append(value)
            if is_all:
                search_filter = f"(objectClass=Person)"
            else:
                search_filter = f"(&(objectClass=Person)({self.attributes.get('username')}={username}))"
            self.conn.search(search_base=self.base_ou,
                             search_filter=search_filter,
                             attributes=_attributes,
                             paged_size=self.paged_size)
            _users_list = list()
            _users_list.extend(self.conn.response)
            # 防止ldap服务器每次最大查询数量1000条限制
            if is_all:
                cookie = self.conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
                while cookie:
                    self.conn.search(search_base=self.base_ou,
                                     search_filter=search_filter,
                                     attributes=_attributes,
                                     paged_size=self.paged_size,
                                     paged_cookie=cookie)
                    _users_list.extend(self.conn.response)
                    cookie = self.conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            if len(_users_list) == 0:
                return ldap_res(message="连接成功 但未查询到LDAP用户", data=[])
            return ldap_res(message="查询成功", data=_users_list)
        except Exception as e:
            return ldap_res(code=0, message=f"{e}", data=[])

    def verify_user(self, user: str, password: str):
        """根据userdn和password验证用户登录"""
        if not self.conn_bind:
            logger.error(self.conn_messagr)
            return ldap_res(code=0, message=self.conn_messagr, data=[])
        try:
            _res = self.conn.rebind(user=user, password=password)
            return ldap_res(code=1 if _res else 0)
        except LDAPInvalidCredentialsResult as e:
            if '52e' in e.message:
                message = '账号密码不正确'
            elif '775' in e.message:
                message = '账号已锁定'
            elif '533' in e.message:
                message = '账号已禁用'
            else:
                message = '认证失败'
            return ldap_res(code=0, message=message)


if __name__ == '__main__':
    test = LdapAuthMixin(hosts=['ldap://192.168.112.128:389'], user='CN=Administrator,CN=Users,DC=fastcow,DC=com',
                         password='guo123.0',
                         base_ou='OU=fastapi,DC=fastcow,DC=com', )

    print(test.search_user(is_all=True))
    print(test.verify_user('CN=张三,OU=运维部,OU=fastapi,DC=fastcow,DC=com', 'guo123.0'))
