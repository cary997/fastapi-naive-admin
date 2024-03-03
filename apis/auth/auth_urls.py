from fastapi import APIRouter
from apis.auth import users_api,roles_api, menus_api

authRouters = APIRouter()
authRouters.include_router(users_api.router)
authRouters.include_router(roles_api.router)
authRouters.include_router(menus_api.router)
