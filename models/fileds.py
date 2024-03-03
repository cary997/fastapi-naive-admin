#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fastapi-naive-admin
@File ：fileds.py
@Author ：Cary
@Date ：2024/2/12 13:10
@Descripttion : "自定义字段"
"""
import datetime
import time
import warnings
from typing import Any, Optional, Union, Type
from pydantic.v1.datetime_parse import parse_datetime
from tortoise import ConfigurationError, timezone
from tortoise.fields.base import Field
from tortoise.timezone import get_timezone, localtime, get_use_tz
from tortoise.models import Model


class UnixDateTimeField(Field[int], int):
    """
    Unix时间戳格式Filed字段，返回int类型的时间戳格式
    """
    SQL_TYPE = "BIGINT"

    class _db_mysql:
        SQL_TYPE = "BIGINT"

    class _db_oracle:
        SQL_TYPE = "INT"

    def __init__(self, is_auto_now: bool = False, is_auto_now_add: bool = False, **kwargs: Any) -> None:
        if is_auto_now_add and is_auto_now:
            raise ConfigurationError("You can choose only 'is_auto_now' or 'is_auto_now_add'")
        super().__init__(**kwargs)
        self.is_auto_now = is_auto_now
        self.is_auto_now_add = is_auto_now | is_auto_now_add

    def to_python_value(self, value: Any) -> Optional[int]:
        if value is None:
            value = None
        else:
            if isinstance(value, datetime.datetime):
                value = value
            elif isinstance(value, int):
                value = datetime.datetime.fromtimestamp(value)
            else:
                value = parse_datetime(value)
            if timezone.is_naive(value):
                value = timezone.make_aware(value, get_timezone())
            else:
                value = localtime(value)
            value = int(value.timestamp())
        self.validate(value)
        return value

    def to_db_value(
            self, value: Optional[datetime.datetime], instance: "Union[Type[Model], Model]"
    ) -> Optional[int]:
        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
                self.is_auto_now
                or (self.is_auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = timezone.now()
            value = int(value.timestamp())
            setattr(instance, self.model_field_name, value)
            return value
        if value is not None:
            if get_use_tz():
                if timezone.is_naive(value):
                    warnings.warn(
                        "DateTimeField %s received a naive datetime (%s)"
                        " while time zone support is active." % (self.model_field_name, value),
                        RuntimeWarning,
                    )
                    value = timezone.make_aware(value, "UTC")
                    value = int(value.timestamp())
        self.validate(value)
        return value

    @property
    def constraints(self) -> dict:
        data = {}
        if self.is_auto_now_add:
            data["readOnly"] = True
        return data

    def describe(self, serializable: bool) -> dict:
        desc = super().describe(serializable)
        desc["is_auto_now_add"] = self.is_auto_now_add
        desc["is_auto_now"] = self.is_auto_now
        return desc
