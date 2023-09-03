# _author: Coke
# _date: 2023/8/30 20:24

from application.api import api
from application import utils, db, models, socketio
from sqlalchemy import or_
from flask import request

import logging
import json


@api.route('/conf/magic/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_magic_list():
    """
    获取魔法变量列表
    :return:
    """

    body = request.get_json(silent=True)

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    keyword = body.get('keyword')
    keyword = keyword if keyword else ""
    data_type = body.get('type')
    node_id = body.get('nodeId')
    node_id = node_id if node_id else 0
    status = body.get('status')

    if not all([page, size, data_type]):
        return utils.rander(utils.DATA_ERR)

    query_list = [
        or_(models.MagicMenu.name.like(f'%{keyword}%'), models.MagicMenu.keyword.like(f'%{keyword}%')),
        models.MagicMenu.node_id == node_id,
        models.MagicMenu.data_type == data_type
    ]

    if isinstance(status, bool):
        query_list.append(models.MagicMenu.status == status)

    data, total = utils.paginate(
        models.MagicMenu,
        page,
        size,
        filter_list=query_list,
        order_by=models.MagicMenu.sort
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(data, total, page, size))


@api.route('/conf/magic/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_magic_info():
    """
    新增/修改魔法变量信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    magic_id = body.get('id')
    name = body.get('name')
    keyword = body.get('keyword')
    sort = body.get('sort')
    desc = body.get('desc')
    status = body.get('status')
    node_id = body.get('nodeId')
    node_id = node_id if node_id else 0
    params = body.get('params')
    params = params if params else []
    data_type = body.get('type')

    if not all([name, keyword, sort, data_type, isinstance(status, bool)]):
        return utils.rander(utils.DATA_ERR)

    if magic_id:
        magic = models.MagicMenu.query.filter_by(id=magic_id)

        if not magic.first():
            return utils.rander(utils.DATA_ERR, '此魔法变量已不存在')

        update_dict = dict(
            name=name,
            keyword=keyword,
            desc=desc,
            status=status,
            sort=sort,
            node_id=node_id,
            params=json.dumps(params, ensure_ascii=False),
            data_type=data_type
        )

        try:
            magic.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        # 通知前端数据更新, 重新获取数据
        socketio.emit('updateMagicVariable')
        return utils.rander(utils.OK)

    magic = models.MagicMenu(name, keyword, sort, desc, status, node_id, data_type, params)
    try:
        db.session.add(magic)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('updateMagicVariable')
    return utils.rander(utils.OK)


@api.route('conf/magic/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_magic_info():
    """
    删除魔法变量信息
    :return:
    """

    socketio.emit('updateMagicVariable')
    return utils.delete(models.MagicMenu, dict(id='id'), dict(node_id='id'))


@api.route('conf/magic/variable', methods=['GET', 'POST'])
@utils.login_required
def get_magic_variable():
    """
    获取动态变量
    :return:
    """

    menu = models.MagicMenu.query.filter_by(status=1, node_id=0, data_type='menu').order_by(models.MagicMenu.sort).all()

    magic_variable_list = []

    for item in menu:
        result = item.result
        result['children'] = assemble(item.id, 'menu')
        result['functionList'] = assemble(item.id, 'function')

        magic_variable_list.append(result)

    return utils.rander(utils.OK, data=magic_variable_list)


def assemble(node_id: int, data_type: str) -> list:
    """ 将子节点中的元素映射id变为元素映射信息 """
    children_list = []
    for children in models.MagicMenu.query.filter_by(
            status=1,
            node_id=node_id,
            data_type=data_type
    ).order_by(models.MagicMenu.sort).all():
        children_result = children.result
        children_result['params'] = [
            models.DynamicElement.query.filter_by(id=element_id).first().result
            for element_id in children_result['params']
        ]
        children_list.append(children_result)

    return children_list
