#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：base.py
@Author ：Cary
@Date ：2024/2/15 23:24
@Descripttion : ""
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union


class BaseResponse(BaseModel):
    code: int = Field(title="状态码")
    message: str = Field(title="提示信息")
    data: Optional[Union[Dict, List]] = Field(default=None, title="数据")