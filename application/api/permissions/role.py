# _author: Coke
# _date: 2022/5/11 15:16

from application import models, db, utils
from application.api import api
from flask import request

import logging
import json


@api.route('/permissions/role/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_permissions_role_info():
    """ 新增/编辑角色信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    role_id = body.get('id')
    name = body.get('name')
    identifier = body.get('identifier')
    permissions_api = body.get('permissionsApi')

    if not all([name, permissions_api, identifier, isinstance(permissions_api, list)]):
        return utils.rander(utils.DATA_ERR)

    # 处理菜单标识符
    menu_list = []
    menu_info = models.Menu.query.filter_by(menu_type='menu').all()
    for items in menu_info:
        for item in permissions_api:
            if item == items.identifier:
                menu_list.append(item)

    # 标识符去重验证
    identifier_info = models.Role.query.filter_by(identifier=identifier).first()
    if identifier_info and identifier_info.id != role_id:
        return utils.rander(utils.DATA_ERR, '标识符不可重复')

    if role_id:
        role_info = models.Role.query.filter_by(id=role_id)
        if not role_info.first():
            return utils.rander(utils.DATA_ERR, '此角色信息不存在')

        update_dict = {
            'name': name,
            'identifier': identifier,
            'permissions_api': json.dumps(permissions_api),
            'permissions_menu': json.dumps(menu_list)
        }
        try:
            role_info.update(update_dict)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    new_role = models.Role(name, identifier, permissions_api, menu_list)
    try:
        db.session.add(new_role)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/permissions/role/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_permissions_role_list():
    """ 获取角色列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    page_size = body.get('pageSize')
    name = body.get('name')
    identifier = body.get('identifier')

    if not all([page, page_size]):
        return utils.rander(utils.DATA_ERR)

    query_list = [
        models.Role.name.like(f'%{name if name else ""}%'),
        models.Role.identifier.like(f'%{identifier if identifier else ""}%')
    ]

    # 当用户非admin角色时列表不再返回admin角色信息
    role_info = utils.get_user_role_info()
    if role_info.identifier != 'admin':
        query_list.append(models.Role.identifier != 'admin')

    role_list, role_total = utils.paginate(
        models.Role,
        page,
        page_size,
        filter_list=query_list
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(role_list, role_total, page, page_size))


@api.route('/permissions/role/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_permissions_role_info():
    """ 删除角色信息 """

    _id = utils.query_id()
    if not _id:
        return utils.rander(utils.DATA_ERR)

    role_info = models.Role.query.filter_by(id=_id)

    if not role_info.first():
        return utils.rander(utils.DATA_ERR, '此角色信息不存在')

    if role_info.first().identifier == 'admin':
        return utils.rander(utils.DATA_ERR, '此角色不可删除')

    try:
        role_info.delete()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
