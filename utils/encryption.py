#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：encryption.py
@Author ：Cary
@Date ：2024/2/15 16:31
@Descripttion : "用于某些功能加解密"
"""

import base64
import re
from Crypto.Cipher import AES
from utils.config import settings


class AESCBC:
    def __init__(self, key, iv):
        self.key = bytes(key, encoding="utf8")
        self.IV = bytes(iv, encoding="utf8")
        self.mode = AES.MODE_CBC
        self.bs = 16  # block size
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def encrypt(self, text):
        generator = AES.new(self.key, self.mode, self.IV)
        try:
            crypt = generator.encrypt(self.PADDING(text).encode('utf-8'))
            crypted_str = base64.b64encode(crypt)  # 输出Base64
            # crypted_str = binascii.b2a_hex(crypt)  # 输出Hex
            data = crypted_str.decode()
            result = {"code": 1, "data": data}
        except Exception as e:
            result = {"code": 0, "data": e}
        return result

    def decrypt(self, text):
        try:
            generator = AES.new(self.key, self.mode, self.IV)
            text += (len(text) % 4) * '='
            decrpyt_bytes = base64.b64decode(text)  # 输出Base64
            # decrpyt_bytes = binascii.a2b_hex(text)  # 输出Hex
            meg = generator.decrypt(decrpyt_bytes)
            # 去除解码后的非法字符
            data = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
            result = {"code": 1, "data": data}
        except Exception as e:
            result = {"code": 0, "data": e}
        return result


if __name__ == '__main__':
    aes = AESCBC(settings.SECRET_KEY, settings.SECRET_IV)
    to_encrypt = 'HLMWS4I2A3SQGUZS7M65PUQSQMAAQIZL'
    str1 = aes.encrypt(to_encrypt)
    str2 = aes.decrypt(str1['data'])
    print(str1)
    print(str2)
