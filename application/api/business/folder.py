# _author: Coke
# _date: 2022/5/27 20:54

from application import db, models, utils
from flask import request
from application.api import api

import logging


@api.route('/business/folder/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_folder_list():
    """ 获取文件夹列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    folder_id = body.get('id')
    project_id = body.get('projectId')
    folder_id = folder_id if folder_id else 0
    special = body.get('special')
    special = True if special is None else special

    if not project_id:
        return utils.rander(utils.DATA_ERR)

    query = {
        'node_id': folder_id,
        'project_id': project_id
    }

    folder = models.Folder.query.filter_by(**query).all()
    folder_dict_list = []
    for items in folder:
        children = items.result
        children['leaf'] = False if models.Folder.query.filter_by(node_id=items.id).first() else True
        children['exist'] = False if models.Case.query.filter_by(module=items.id, special=special).first() else True
        folder_dict_list.append(children)

    return utils.rander(utils.OK, data=folder_dict_list)


@api.route('/business/folder/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_folder_info():
    """ 新增/修改文件夹信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    node_id = body.get('nodeId')
    name = body.get('name')
    module_id = body.get('id')
    project_id = body.get('projectId')
    node_id = node_id if node_id else 0

    if not all([name, project_id]):
        return utils.rander(utils.DATA_ERR, '名称不可为空')

    # 验证是否数据重复
    modules = models.Folder.query.filter_by(name=name, node_id=node_id).first()
    if modules and module_id != modules.id:
        return utils.rander(utils.DATA_ERR, '名称不可重复')

    # 修改
    if module_id:
        module_info = models.Folder.query.filter_by(id=module_id)
        if not module_info.first():
            return utils.rander(utils.DATA_ERR, '此模块不存在')

        try:
            module_info.update(dict(name=name))
            db.session.flush()
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander(utils.DATABASE_ERR)
        items = module_info.first().result
        items['leaf'] = True
        return utils.rander(utils.OK, data=items)

    module_info = models.Folder.query.filter_by(id=node_id).first()

    # 校验关系分类是否存在
    if node_id and not module_info:
        return utils.rander(utils.DATA_ERR, '无此父级关系分类')

    # 创建关系分类深度校验
    if module_info and module_info.node_id != 0:
        return utils.rander(utils.DATA_ERR, '最多只允许创建二级关系分类')

    # 数据创建
    new_module = models.Folder(
        project_id=project_id,
        name=name,
        node_id=node_id
    )

    # 处理数据库存储异常
    try:
        db.session.add(new_module)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)
    items = new_module.result
    items['leaf'] = True
    return utils.rander(utils.OK, data=items)


@api.route('/business/folder/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_folder_info():
    """ 删除模块信息 """

    return utils.delete(models.Folder, dict(id='id'), dict(node_id='id'))
