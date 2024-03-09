#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

@File ：users_schema.py
@Author ：Cary
@Date ：2024/2/17 21:48
@Descripttion : ""
"""
import math
from fastapi import APIRouter, Request, Query, BackgroundTasks
from core.Exeption.Response import fail, success
from extend.redis.init import redisCache
from schemas.auth import users_schema
from models.auth.model import AuthUsers
from models.auth.model import AuthRoles
from schemas.base import BaseResponse
from utils.cache_tools import get_redis_data
from utils.password_tools import get_password_hash, generate_password
from extend.sends.send_mail import sys_send_mail

router = APIRouter(prefix='/users')


@router.post('/add', summary="创建用户", response_model=users_schema.UserCreateResponse)
async def auth_users_add(create_content: users_schema.UserCreateRequest):
    """
    创建用户
    :param create_content:
    :return:
    """
    # 过滤用户
    get_user = await AuthUsers.get_or_none(username=create_content.username)
    # 判断用户是否存在
    if get_user:
        return fail(message=f"用户 {create_content.username} 已经存在!")
    # 密码hash
    create_content.password = get_password_hash(create_content.password)
    # 创建用户
    add_user = await AuthUsers.create(**create_content.model_dump(exclude={'roles'}))

    # 判断是否创建成功
    if not add_user:
        return fail(message="创建失败!")
    # roles列表
    roles = create_content.roles
    # 添加roles
    if roles:
        await add_user.roles.clear()
        roles_list = await AuthRoles.filter(id__in=roles)
        await add_user.roles.add(*roles_list)
    # 序列化返回结果
    form_add_user = await users_schema.UserCreateResult.from_tortoise_orm(add_user)
    result = form_add_user.model_dump()
    result['roles'] = roles
    return success(message="创建成功", data=result)


@router.delete('/del/{user_id}', summary="删除用户", response_model=users_schema.UserDeleteResponse)
async def auth_users_del(request: Request, user_id: int):
    """
    删除用户
    :param request:
    :param user_id:
    :return:
    """
    if request.state.user_id == user_id:
        return fail(message="您不能将自己删除")
    delete_action = await AuthUsers.filter(pk=user_id).delete()
    if not delete_action:
        return fail(message="删除失败", data={"id": user_id})
    # 删除redis中的token 强制下线
    cache: redisCache = request.app.state.cache
    await cache.delete(f"jwt:{user_id}")
    return success(message="删除成功", data={"id": user_id})


@router.delete('/bulkdel', summary="批量删除用户", response_model=users_schema.UserBulkDeleteResponse)
async def auth_users_bulkdel(request: Request, data: users_schema.UserBulkDeleteRequest):
    """
    删除用户
    :param request:
    :param data:
    :return:
    """
    user_list = data.user_list
    if request.state.user_id in user_list:
        return fail(message="您不能将自己删除")
    users = await AuthUsers.filter(pk__in=user_list)
    res_list = []
    if len(users) == 0:
        return fail(message="无法查询到指定用户", data=res_list)

    for user in users:
        res_list.append(user.id)
        await user.delete()
        # 删除redis中的token 强制下线
        cache: redisCache = request.app.state.cache
        await cache.delete(f"jwt:{user.id}")
    return success(message="删除成功", data=res_list)


@router.patch('/set/{user_id}', summary="更新用户", response_model=users_schema.UserUpdateResponse)
async def auth_users_set(request: Request, user_id: int, update_content: users_schema.UserUpdateRequest):
    """
    更新用户
    :param request:
    :param user_id:
    :param update_content:
    :return:
    """
    # 判断用户是否存在
    if request.state.user_id == user_id and isinstance(update_content.user_status,
                                                       bool) and not update_content.user_status:
        return fail(message="您不能将自己禁用")
    get_user = await AuthUsers.get_or_none(pk=user_id)
    if not get_user:
        return fail(message="用户不存在")

    # 获取roles id列表
    roles = update_content.roles
    # 判断是否更新角色
    update_roles = update_content.update_roles

    # 更新用户
    update_user = await get_user.update_from_dict(
        update_content.model_dump(exclude_unset=True, exclude={'roles', 'update_roles'}))
    await update_user.save()

    if update_roles:
        # 先将角色清空
        await update_user.roles.clear()
    # 更新roles
    if roles:
        roles_list = await AuthRoles.filter(id__in=roles)
        await update_user.roles.add(*roles_list)
    # 序列化
    form_update_user = await users_schema.UserUpdateResult.from_tortoise_orm(update_user)
    result = form_update_user.model_dump()
    if result.get('user_status') is False:
        # 删除redis中的token 强制下线
        cache: redisCache = request.app.state.cache
        await cache.delete(f"jwt:{user_id}")
    result['roles'] = roles
    return success(message='更新成功', data=result)


@router.patch('/bulkset', summary="批量更新用户", response_model=users_schema.UserBulkUpdateResponse)
async def auth_users_bulkset(request: Request, update_content: users_schema.UserBulkUpdateRequest):
    # 获取要更新的字段
    update_fields = []
    # 排除的字段
    exclude_fields = ["user_list", "update_roles"]
    # 获取要更新的字段
    for k, v in update_content.model_dump().items():
        if k not in exclude_fields and v is not None:
            update_fields.append(k)
    if len(update_fields) == 0:
        return fail(message="未获取到支持的更新字段 user_type | user_status | roles ")
    # 查询要更新的用户
    user_list = update_content.user_list

    if request.state.user_id in user_list and isinstance(update_content.user_status,
                                                         bool) and not update_content.user_status:
        return fail(message="您不能将自己禁用")
    users = await AuthUsers.filter(pk__in=user_list)
    res_list = []
    if len(users) == 0:
        return fail(message="无法查询到指定用户", data=res_list)
    # 判断是否更新角色
    update_roles = update_content.update_roles
    # redis中缓存的kye 如果禁用要删除
    cache_kye = []
    for user in users:
        if "roles" in update_fields:
            roles = update_content.roles
            if update_roles:
                # 先将角色清空
                await user.roles.clear()
            if roles:
                roles_list = await AuthRoles.filter(id__in=roles)
                await user.roles.add(*roles_list)
        if "user_status" in update_fields:
            user.user_status = update_content.user_status
            if update_content.user_status is False:
                cache_kye.append(f"jwt:{user.id}")
        if "user_type" in update_fields:
            user.user_type = update_content.user_type
        res_list.append(user.pk)
    # 角色字段为多对多无法使用bulk_update方法
    if "roles" in update_fields:
        update_fields.remove("roles")
    # 删除角色字段后还存在其他字段则批量更新
    if update_fields:
        # DB中批量更新
        await AuthUsers.bulk_update(users, fields=update_fields)
        if update_content.user_status is False:
            # redis中批量删除token
            cache: redisCache = request.app.state.cache
            p_cache = cache.pipeline()
            p_cache.delete(*cache_kye)
            await p_cache.execute()
    return success(message='更新完成', data=res_list)


@router.get('/query', summary="过滤用户列表", response_model=users_schema.UserQueryResponse)
async def auth_users_query(
        username: str = Query(None),
        nickname: str = Query(None),
        phone: str = Query(None),
        email: str = Query(None),
        user_type: int = Query(None),
        user_status: bool = Query(None),
        roles: int = Query(None),
        limit: int = 10,
        page: int = 1,
        order_by: str = "username"
):
    """
    过滤用户
    """
    # 序列化查询参数
    query = {}
    if username:
        query.setdefault('username', username)
    if nickname:
        query.setdefault('nickname', nickname)
    if phone:
        query.setdefault('phone', phone)
    if email:
        query.setdefault('email', email)
    if user_type:
        query.setdefault('user_type', user_type)
    if user_status:
        query.setdefault('user_status', user_status)
    if roles:
        query.setdefault('roles', roles)
    # 查询结果
    query_data = AuthUsers.filter(**query).all()
    # 结果总数
    query_total = await query_data.count()
    if not query_total:
        return success(message="查询结果为空!")
    # 分页总数
    page_total = math.ceil(query_total / limit)
    if page > page_total:
        return fail(message="输入页数大于分页总数!")

    # 分页排序
    query_result = query_data.limit(limit).offset(limit * (page - 1)).order_by(order_by)

    form_query_data = await users_schema.UserQuerySet.from_queryset(query_result)
    # 过滤角色使user['roles']中只包含关联角色的id
    result = []
    for user in form_query_data.model_dump():
        if user.get('roles'):
            user['roles'] = [roles['id'] for roles in user['roles']]
        result.append(user)
    # 序列化查询结果
    result = {
        "result": result,
        "total": query_total,
        "page_total": page_total,
        "page": page,
        "limit": limit
    }
    return success(message=f"查询成功", data=result)


@router.get('/get', summary="查询当前用户", response_model=users_schema.UserGetResponse)
async def auth_users_get(request: Request):
    """
    查询用户
    :return:
    """
    get_user = await AuthUsers.get_or_none(pk=request.state.user_id)
    if not get_user:
        return fail(message="用户不存在")
    format_user = await users_schema.UserGetResult.from_tortoise_orm(get_user)
    result = format_user.model_dump()
    return success(message="用户查询成功", data=result)


@router.post('/pwdset', summary="修改密码", response_model=BaseResponse)
async def auth_users_pwdset(request: Request, req_data: users_schema.UserSetPasswordRequest,
                            background_tasks: BackgroundTasks):
    """
    修改密码

    `
    如果is_reset为true则自动生成并重置用户密码
    `

    :param request:
    :param req_data:
    :param background_tasks
    :return:
    """
    user_id = req_data.user_id
    get_user = await AuthUsers.get_or_none(pk=user_id)
    if not get_user:
        return fail(message="用户不存在")
    # 如果是重置密码则自动生成随机密码并更新用户密码
    if req_data.is_reset:
        new_password = generate_password(12)
        await AuthUsers.filter(pk=user_id).update(password=get_password_hash(new_password))
        if get_user.email:
            # 配置了邮件就后台异步发送邮件通知不返回结果
            background_tasks.add_task(sys_send_mail, recipients=get_user.email,
                                      body={'title': "密码重置完成", 'username': get_user.nickname,
                                            "message": f"新的密码为 <font color='#8e97fd'>{new_password}</font> 请在登录后立即修改密码，以避免您的密码泄露！"},
                                      subject="重置密码通知", template_name="email.html")
        return success(message="重置成功", data={'new_password': new_password})
    else:
        if user_id != request.state.user_id:
            return fail(message="您不能修改别人的密码")
        password = req_data.password
        repassword = req_data.repassword
        if password != repassword:
            return fail(message="两次密码不一致")
        await AuthUsers.filter(pk=user_id).update(password=get_password_hash(password))
        return success(message="修改成功")


@router.post('/otpreset/{user_id}', summary="重置TOTP", response_model=BaseResponse)
async def auth_users_otpreset(user_id: int, background_tasks: BackgroundTasks):
    """
    查询用户
    :param user_id
    :param background_tasks
    :return:
    """
    security = await get_redis_data("sys:settings", 'security')
    _totp = security.get('totp') if security else None
    if not _totp:
        return fail(message="系统未开启MFA登录")
    get_user = await AuthUsers.get_or_none(pk=user_id)
    if not get_user:
        return fail(message="用户不存在")
    get_user.totp = None
    await get_user.save()
    if get_user.email:
        # 配置了邮件就异步发送邮件通知不返回结果
        background_tasks.add_task(sys_send_mail, recipients=get_user.email,
                                  body={'title': "TOTP令牌重置完成", 'username': get_user.nickname,
                                        "message": "请重新登录您的账户，系统将自动提示您绑定令牌，请按照系统提示完成绑定！"},
                                  subject="重置TOTP通知", template_name="email.html")

    return success(message="重置成功")
