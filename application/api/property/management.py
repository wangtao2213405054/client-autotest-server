# _author: Coke
# _date: 2022/5/1 20:16

from application.api import api
from application import db, models
from flask import request
from application.utils.response import rander, paginate_structure
from application.utils.token import login_required
from application.utils.permissions import get_user_role_info, permissions_required

import re
import logging
import json


@api.route('/account/user/edit', methods=['POST', 'PUT'])
@login_required
@permissions_required
def edit_user_info():
    """ 新增/修改 用户信息 """

    body = request.get_json()
    if not body:
        return rander('BODY_ERR')

    user_id = body.get('id')
    name = body.get('name')
    email = body.get('email')
    mobile = body.get('mobile')
    password = body.get('password')
    avatar_url = body.get('avatarUrl')
    state = body.get('state')
    department = body.get('department')
    role = body.get('role')

    if not all([name, email, mobile, department]):
        return rander('DATA_ERR')

    if not isinstance(department, list):
        return rander('DATA_ERR')

    node = department[-1]
    department = json.dumps(department)

    # 判断账号是否为邮箱
    if not re.search('@', email) or len(email) > 64:
        return rander('DATA_ERR', '邮箱格式不正确')

    # 验证手机号格式
    if not re.match(r"1[23456789]\d{9}", mobile):
        return rander('MOBILE_ERR')

    # 验证邮箱是否重复
    user_info = models.User.query.filter_by(email=email).first()
    if user_info and user_info.id != user_id:
        return rander('DATA_ERR', '此邮箱已存在')

    # 验证手机号是否重复
    user_info = models.User.query.filter_by(mobile=mobile).first()
    if user_info and user_info.id != user_id:
        return rander('DATA_ERR', '此手机号已存在')

    # 验证角色信息
    role_info = models.Role.query.get(role)
    if not role_info:
        return rander('DATA_ERR', '角色信息不存在')
    current_role = get_user_role_info()
    if role_info.identifier == 'admin' and current_role.identifier != 'admin':
        return rander('ROLE_ERR', '角色权限不足')

    # 修改
    if user_id:
        update_user = {
            'name': name,
            'email': email,
            'mobile': mobile,
            'avatar_url': avatar_url,
            'node': node,
            'department': department,
            'role': role,
            'state': state
        }
        try:
            models.User.query.filter_by(id=user_id).update(update_user)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return rander('DATABASE_ERR')

        return rander('OK')

    # 新增
    new_user = models.User(
        name=name,
        email=email,
        mobile=mobile,
        password=password,
        avatar_url=avatar_url,
        node=node,
        department=department,
        role=role
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return rander('DATABASE_ERR')

    return rander('OK')


@api.route('/account/user/list', methods=['GET', 'POST'])
@login_required
@permissions_required
def get_user_list():
    """ 获取用户列表 """

    body = request.get_json()

    if not body:
        return rander('BODY_ERR')

    classification_id = body.get('id')
    page = body.get('page')
    page_size = body.get('pageSize')
    name = body.get('name')
    mobile = body.get('mobile')
    state = body.get('state')

    if not all([page, page_size]):
        return rander('DATA_ERR')

    # 获取级别信息
    son_id_list = [classification_id]
    classification_info = models.Classification.query.filter_by(id=classification_id).first()

    # 如果是父级信息则去便利其所有的子集
    if classification_info and not classification_info.node_id:
        son_info = models.Classification.query.filter_by(node_id=classification_info.id).all()
        for item in son_info:
            son_id_list.append(item.id)

    # 数据过滤
    query_info = [
        models.User.node.in_(son_id_list) if classification_id else models.User.id,
        models.User.name.like(f'%{name if name else ""}%'),
        models.User.mobile.like(f'%{mobile if mobile else ""}%')
    ]
    if isinstance(state, bool):
        query_info.append(state)

    # 如果 classification_id 为真则为指定查询, 否则返回全部用户
    user = models.User.query.filter(*query_info)
    user_list = user.order_by(models.User.id.desc()).paginate(page, page_size, False)
    total = user.count()

    user_dict_list = []
    for item in user_list.items:
        user_dict_list.append(item.to_dict())

    return rander('OK', data=paginate_structure(user_dict_list, total, page, page_size))


@api.route('/account/user/delete', methods=['POST', 'DELETE'])
@login_required
@permissions_required
def delete_user_info():
    """ 删除用户接口 """

    body = request.get_json()

    if not body:
        return rander('BODY_ERR')

    user_id = body.get('id')

    if not user_id and not isinstance(user_id, list):
        return rander('DATA_ERR')

    try:
        for item in user_id:
            models.User.query.filter_by(id=item).delete()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return rander('DATABASE_ERR')

    return rander('OK')


@api.route('/account/user/ids', methods=['GET', 'POST'])
@login_required
@permissions_required
def get_user_list_by_ids():
    """ 通过id list 获取对应的用户信息 """

    body = request.get_json()

    if not body:
        return rander('BODY_ERR')

    id_list = body.get('idList')

    if not isinstance(id_list, list):
        return rander('DATA_ERR')

    user_dict_list = []
    for item in id_list:
        user_dict_list.append(models.User.query.get(item).to_dict())

    return rander('OK', data=user_dict_list)
