
from application.api import api, swagger
from flask import request, g
from application import models, utils
# from sqlalchemy.orm.query import Query

import json


@api.route('/user/login', methods=['POST'])
@swagger('userLogin.yaml')
def user_login():
    """ 登录 """
    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    email = body.get('username')
    password = body.get('password')

    if not all([email, password]):
        return utils.rander(utils.DATA_ERR)

    user_info = models.User.query.filter_by(email=email).first()

    if not user_info or user_info.password != password:
        return utils.rander(utils.DATA_ERR, '用户名或密码错误')

    token = utils.create_token(user_id=user_info.id, username=user_info.name)
    user_info = user_info.result
    user_info['token'] = token
    return utils.rander(utils.OK, data=user_info)


@api.route('/user/info', methods=['GET', 'POST'])
@utils.login_required
@swagger('userInfo.yaml')
def get_user_info():
    """ 获取个人信息 """
    user_info = models.User.query.filter_by(id=g.user_id).first()
    role_info = models.Role.query.filter_by(id=user_info.role).first()

    roles = []
    if role_info:
        if role_info.identifier == 'admin':
            roles.append('admin')
        else:
            roles = json.loads(role_info.permissions_menu) + json.loads(role_info.permissions_api)

    user_info = user_info.result
    user_info['roles'] = roles
    return utils.rander(utils.OK, data=user_info)
