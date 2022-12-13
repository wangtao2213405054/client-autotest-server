# _author: Coke
# _date: 2022/5/9 17:41

from application.api import api
from application import db, models, utils
from flask import request

import logging


@api.route('/permissions/menu/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_permissions_menu_info():
    """ 新增/修改权限菜单 """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    menu_id = body.get('id')
    node_id = body.get('nodeId')
    name = body.get('name')
    identifier = body.get('identifier')
    menu_type = body.get('menuType')
    belong_type = body.get('belongType')

    if not all([name, identifier]):
        return utils.rander('DATA_ERR')

    if not node_id:
        node_id = 0

    # 过滤标识符是否重复
    menu_info = models.Menu.query.filter_by(identifier=identifier).first()
    if menu_info and menu_info.id != menu_id:
        return utils.rander('DATA_ERR', '此标识符已存在')

    # 查看名称是否重复
    menu_info = models.Menu.query.filter_by(node_id=node_id).all()
    for item in menu_info:
        if name == item.name and item.id != menu_id:
            return utils.rander('DATA_ERR', '名称不能重复')

    if menu_id:
        menu_info = models.Menu.query.filter_by(id=menu_id)
        if not menu_info.first():
            return utils.rander('DATA_ERR', '此信息已不存在')

        update_data = {
            'name': name,
            'identifier': identifier,
            'menu_type': menu_type,
            'belong_type': belong_type
        }

        try:
            menu_info.update(update_data)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander('DATABASE_ERR')

        return utils.rander('OK')

    menu_info = models.Menu.query.filter_by(id=node_id).first()

    if node_id and not menu_info:
        return utils.rander('DATA_ERR', '无此父级节点')

    try:
        menu_new = models.Menu(
            name=name,
            identifier=identifier,
            menu_type=menu_type,
            belong_type=belong_type,
            node_id=node_id
        )
        db.session.add(menu_new)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


def get_menu_tree(node_id, query_name='', query_identifier=''):
    """ 递归遍历所有子树信息 """
    menu_dict_list = []

    query_dict = []
    if query_name or query_identifier:
        query_dict.append(models.Menu.name.like(f'%{query_name}%'))
        query_dict.append(models.Menu.identifier.like(f'%{query_identifier}%'))
    else:
        query_dict.append(models.Menu.node_id == node_id)

    menu_list = models.Menu.query.filter(*query_dict).all()

    for items in menu_list:
        father = items.to_dict
        father['children'] = get_menu_tree(items.id)

        menu_dict_list.append(father)

    return menu_dict_list


@api.route('/permissions/menu/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_permissions_menu_list():
    """ 获取权限菜单列表 """

    body = request.get_json()

    if not body:
        body = {}

    name = body.get('name')
    identifier = body.get('identifier')
    return utils.rander('OK', data=get_menu_tree(0, name, identifier))


def delete_menu_tree(node_id):
    """ 便利删除树信息 """
    menu_dict_list = []
    if node_id not in menu_dict_list:
        menu_dict_list.append(node_id)

    menu_list = models.Menu.query.filter_by(node_id=node_id).all()
    for item in menu_list:
        menu_dict_list.append(item.id)

        children = delete_menu_tree(item.id)
        for items in children:
            menu_dict_list.append(items)

    return menu_dict_list


@api.route('/permissions/menu/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_permissions_menu_info():
    """ 删除权限菜单信息 """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    menu_id = body.get('id')

    if not menu_id:
        return utils.rander('DATA_ERR')

    delete_list = delete_menu_tree(menu_id)
    for item in delete_list:
        models.Menu.query.filter_by(id=item).delete()

    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')
