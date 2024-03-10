#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：init_log.py
@Author ：Cary
@Date ：2024/2/8 15:45
@Descripttion : "初始化log配置"
"""
import logging
import os
import sys

from utils.config import settings
from .cusotm_log import InterceptHandler, format_record
from loguru import (
    logger,
    _string_parsers as string_parser
)
from datetime import (
    datetime,
    timedelta
)


class Rotator:
    def __init__(self, str_size, str_time):
        self._size = string_parser.parse_size(str_size)
        at = string_parser.parse_time(str_time)
        now = datetime.now()
        today_at_time = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        if now >= today_at_time:
            # the current time is already past the target time so it would rotate already
            # add one day to prevent an immediate rotation
            self._next_rotate = today_at_time + timedelta(days=1)
        else:
            self._next_rotate = today_at_time

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size:
            return True
        if message.record["time"].timestamp() > self._next_rotate.timestamp():
            self._next_rotate += timedelta(days=1)
            return True
        return False


def init_logs():
    LOG_LEVER = settings.LOG_LEVER
    # uvicorn日志捕获
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )

    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    # 这里的操作是为了改变uvicorn默认的logger，使之采用loguru的logger
    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # 日志文件路径
    applog = settings.LOG_PATH

    # 初始化日志切割函数
    rotator = Rotator(settings.LOG_ROTATION_SIZE, settings.LOG_ROTATION_TIME)

    # 配置loguru的日志句柄，sink代表输出的目标
    handlers = [
        {"sink": applog, "level": LOG_LEVER, "format": format_record, "rotation": rotator.should_rotate,
         "retention": settings.LOG_RETENTION, "enqueue": True, "diagnose": True, "backtrace": True},
    ]

    # 判断是否输出到文件
    if settings.LOG_FILE:
        # 添加记录器
        logger.add(applog, enqueue=True, diagnose=True, backtrace=True, rotation=rotator.should_rotate,
                   retention=settings.LOG_RETENTION,
                   level=LOG_LEVER)
        logger.configure(handlers=handlers)
        # 如果目录不存在则创建
        if not os.path.exists(settings.LOG_PATH):
            os.mkdir(settings.LOG_PATH)
        logger.success('日志记录器初始化')
        logger.success(f'日志路径：{settings.LOG_PATH}')
    # 判断是否输出控制台
    if settings.LOG_CONSOLE:
        if settings.LOG_FILE:
            handlers.append({"sink": sys.stdout, "level": LOG_LEVER, "format": format_record})
        else:
            handlers = [
                {"sink": sys.stdout, "level": LOG_LEVER, "format": format_record}
            ]
        logger.configure(handlers=handlers)
