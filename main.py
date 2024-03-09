#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：main.py
@Author ：Cary
@Date ：2024/2/1 15:45
@Descripttion : "入口文件"
"""

import uvicorn
from fastapi import FastAPI, status
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.Exeption import Exception
from core.Middleware.RequestIpChaeckMiddleware import RequestIpChaeckMiddleware
from core.Middleware.RequestLogMiddleware import RequestLogMiddleware
from utils.config import settings
from core.Events import start_events, shutdown_events
from core.LogManage.init_log import init_logs

# 实例化fastapi
app = FastAPI(
    description=f"""{settings.SYS_DESCRIOTION}""",
    title=settings.SYS_TITLE,
    version=settings.SYS_VERSION,
    docs_url=None,
    redoc_url=None,
    openapi_url=settings.SYS_OPENAPI_URL,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Exception.Http422ErrorResponse}}
)

# 日志初始化
init_logs()

# 添加中间件
# 检查非法IP
app.add_middleware(RequestIpChaeckMiddleware)
# 跨域
app.add_middleware(CORSMiddleware,
                   allow_origins=settings.CORS_ORIGINS,
                   allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
                   allow_methods=settings.CORS_ALLOW_METHODS,
                   allow_headers=settings.CORS_ALLOW_HEADERS)
# 打印请求日志
app.add_middleware(RequestLogMiddleware)

# 事件添加
app.add_event_handler("startup", start_events.startup(app))
app.add_event_handler("shutdown", shutdown_events.stopping(app))

# API文档
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(f"{settings.SYS_ROUTER_PREFIX}/docs", summary="Swagger API文档", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        title=app.title + " Docs",
        openapi_url=app.openapi_url,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/docs-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/docs-ui/swagger-ui.css",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai",
            "displayOperationId": True,
            "filter": True,
            # 控制页面上是否显示Schemas -1不显示
            # "defaultModelsExpandDepth": -1
        },
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f"{settings.SYS_ROUTER_PREFIX}/redoc", summary="Redoc APi文档", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " ReDoc",
        redoc_js_url="/static/docs-ui/redoc.standalone.js",
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
