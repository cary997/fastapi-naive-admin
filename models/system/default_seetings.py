#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：default_seetings.py
@Author ：Cary
@Date ：2024/2/26 23:14
@Descripttion : ""
"""
default_settings = {
    'general': {
        "user_default_password": "FastNaive@2024",
        "watermark": False,
        "watermarkContent": 1,
        "watermarkSize": 2
    },
    'security': {
        "totp": False,
        "ip_check": False,
        "ip_check_mode": 1,
        "ip_black_list": [],
        "ip_white_list": []
    },
    'channels': {
        'email': {
            'MAIL_SERVER': None,
            'MAIL_PORT': None,
            'MAIL_USERNAME': None,
            'MAIL_PASSWORD': None,
            'MAIL_FROM': None,
            'MAIL_FROM_NAME': None,
            'MAIL_STARTTLS': True,
            'MAIL_SSL_TLS': False,
            'USE_CREDENTIALS': True,
            'VALIDATE_CERTS': True
        }
    }
}
