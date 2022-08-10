# _author: Coke
# _date: 2022/5/13 16:38

from flask import g, request
from application import models
from application.utils.response import rander
from application import API_URL_PREFIX

import functools
import json
import re


def get_user_role_info():
    """ 返回当前访问用户的角色信息对象 """
    role_id = models.User.query.get(g.user_id).role
    role_info = models.Role.query.get(role_id)
    return role_info


def permissions_required(view_func):
    """ token 校验装饰器 """
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        current_role = get_user_role_info()
        role_menu = json.loads(current_role.permissions_api)
        identifier = re.sub(API_URL_PREFIX, '', str(request.url_rule))  # 获取当前访问接口的路由信息
        if current_role.identifier != 'admin' and identifier not in role_menu:
            return rander('ROLE_ERR', f'{current_role.name}角色无此接口访问权限')

        return view_func(*args, **kwargs)

    return wrapper
