#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""

@File ：send_mail.py
@Author ：Cary
@Date ：2024/3/1 4:00
@Descripttion : ""
"""
import asyncio
import json
from pathlib import Path

import fastapi_mail.errors
from loguru import logger
from fastapi import APIRouter
from pydantic import EmailStr, BaseModel, DirectoryPath
from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from utils.cache_tools import get_redis_data
from utils.config import settings
from utils.password_tools import is_decrypt, aes_decrypt_password


class SendMail(object):
    def __init__(self, subject: str, body: str | dict, recipients: str | List[str],
                 config: dict = None,
                 subtype: MessageType = "html",
                 template_folder: Optional[DirectoryPath] = None, template_name: Optional[str] = None,
                 **kwargs):
        """
        subject: 主题
        config: 邮件服务器配置
        body: 正文，为str直接解析为dict则需配合template_folder使用jinja2
        recipients: 接收人或接收人列表
        subtype：邮件的子类型默认为html
        template_folder: 模板文件夹路径为None不使用
        template_name: 模板名称
        supperss_send: 测试发送值为1则模拟发送
        """
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.subtype = subtype
        self.config = config
        self.template_folder = template_folder
        self.template_name = template_name
        self.kwargs = kwargs

    async def get_config(self):
        # config_cache = await get_redis_data('sys:settings', 'channels.email')
        if self.config is None:
            return None
        self.config['TEMPLATE_FOLDER'] = self.template_folder
        _config = ConnectionConfig(**self.config)

        return _config

    async def get_messages(self):
        if self.subtype == 'html':
            subtype = MessageType.html
        else:
            subtype = MessageType.plain
        if isinstance(self.recipients, str):
            self.recipients = [self.recipients]
        attachments = []
        if isinstance(self.body, dict):
            self.body['sys_title'] = settings.SYS_TITLE
            self.body["sys_link"] = settings.SYS_LINK
            attachments = [
                {
                    "file": f"{settings.BASE_TEMPLATES_DIR}/logo.png",
                    "headers": {
                        "Content-ID": "<logo>",
                        "Content-Disposition": "inline; filename=\"logo.png\"",
                        # For inline images only
                    },
                    "mime_type": "image",
                    "mime_subtype": "png",
                }
            ]
        bodyData = {
            'body': self.body if isinstance(self.body, str) else None,
            'template_body': self.body if isinstance(self.body, dict) else None,
        }
        message = MessageSchema(subject=self.subject, subtype=subtype, recipients=self.recipients,
                                attachments=attachments, **bodyData,
                                **self.kwargs)
        return message

    async def send(self):
        try:
            _config = await self.get_config()
            if _config is None:
                return {'code': 0, 'message': "请配置邮件服务器  "}
            _message = await self.get_messages()
            instance = FastMail(_config)
            await instance.send_message(_message, template_name=self.template_name)
            return {'code': 1, 'message': "发送成功"}
        except fastapi_mail.errors.ConnectionErrors as e:
            return {'code': 0, 'message': f"连接失败 -- {e}"}
        except Exception as e:
            return {'code': 0, 'message': f"发送失败 -- {e}"}


async def sys_send_mail(
        recipients: str | List[str], body: str | dict, subject: str,
        template_name: str = None, config: dict = None,
        template_folder: Optional[DirectoryPath] = settings.BASE_TEMPLATES_DIR,
):
    if config is None:
        _config = await get_redis_data('sys:settings', 'channels.email')
    else:
        _config = config
    if _config is None:
        return False
    elif _config.get('MAIL_SERVER') is None:
        return False
    if is_decrypt(_config.get('MAIL_PASSWORD')):
        _config['MAIL_PASSWORD'] = aes_decrypt_password(_config.get('MAIL_PASSWORD'))
    _send = SendMail(recipients=recipients, subject=subject, body=body, config=_config,
                     template_folder=template_folder, template_name=template_name)
    _res = await _send.send()
    if _res.get('code'):
        log = logger.success
    else:
        log = logger.error
    log(f"邮件{_res.get('message')} | 接收人 - {recipients} | 通知类型 - {subject}")
    return _res


if __name__ == '__main__':
    asyncio.run(sys_send_mail(recipients="test@163.com",
                              body={'title': "密码重置完成", 'username': "test", "message": "新的密码为 asdasdsad"},
                              subject="系统通知-重置密码", template_name="email.html"))
