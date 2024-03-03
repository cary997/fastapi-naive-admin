#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：config.py
@Author ：Cary
@Date ：2024/2/3 19:18
@Descripttion : "加载config.yaml"
"""

import yaml
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load(file=os.path.join(BASE_DIR, 'config.yaml')):
    """
    载入yaml文件
    :param file:指定文件名
    :return:
    """

    try:
        # 读取配置文件
        yaml_file = open(file, 'r',encoding='utf-8')
        # 转换为dict格式
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return config
    except IOError  as e:
        return "读取的文件不存在：{}".format(file)


if __name__ == '__main__':
    print(BASE_DIR)
    print(load())
