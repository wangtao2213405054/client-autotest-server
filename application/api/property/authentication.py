
from application.api import api
from flask import request, g
from application import models, utils

import json
# from sqlalchemy.orm.query import Query


@api.route('/user/login', methods=['POST', 'GET'])
def user_login():

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    email = body.get('username')
    password = body.get('password')

    if not all([email, password]):
        return utils.rander('DATA_ERR')

    user_info = models.User.query.filter_by(email=email).first()

    if not user_info or user_info.password != password:
        return utils.rander('DATA_ERR', '用户名或密码错误')

    token = utils.create_token(user_id=user_info.id, user_name=user_info.name)
    user_info = user_info.to_dict()
    user_info['token'] = token
    return utils.rander('OK', data=user_info)


@api.route('/user/info', methods=['GET', 'POST'])
@utils.login_required
def get_user_info():
    """ 获取个人信息 """
    user_info = models.User.query.filter_by(id=g.user_id).first()
    role_info = models.Role.query.filter_by(id=user_info.role).first()

    roles = []
    if role_info:
        if role_info.identifier == 'admin':
            roles.append('admin')
        else:
            roles = json.loads(role_info.permissions_menu)

    user_info = user_info.to_dict()
    user_info['roles'] = roles
    return utils.rander('OK', data=user_info)
