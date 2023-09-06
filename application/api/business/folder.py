# _author: Coke
# _date: 2022/5/27 20:54

from application import db, models, utils
from flask import request
from application.api import api, swagger

import logging


def get_folder_hierarchy(node_id, project_id):
    """ 递归查询当前项目下的所有文件夹及测试用例 """

    query = dict(project_id=project_id, node_id=node_id)
    submodules = models.Folder.query.filter_by(**query).order_by(models.Folder.sort).all()
    hierarchy = []
    for submodule in submodules:
        folder = submodule.result
        children = get_folder_hierarchy(submodule.id, project_id)
        if children:
            folder['children'] = children

        hierarchy.append(folder)

    return hierarchy


@api.route('/business/folder/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('folderList.yaml')
def get_folder_list():
    """ 获取文件夹列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')

    if not project_id:
        return utils.rander(utils.DATA_ERR)

    hierarchy = get_folder_hierarchy(0, project_id)
    return utils.rander(utils.OK, data=hierarchy)


@api.route('/business/folder/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('folderEdit.yaml')
def edit_folder_info():
    """ 新增/修改文件夹信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    node_id = body.get('nodeId')
    name = body.get('name')
    module_id = body.get('id')
    project_id = body.get('projectId')
    data_type = body.get('type')
    data_type = data_type if data_type else 'folder'
    node_id = node_id if node_id else 0

    if not all([name, project_id]):
        return utils.rander(utils.DATA_ERR)

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
        return utils.rander(utils.OK, data=items)

    module_info = models.Folder.query.filter_by(id=node_id).first()

    # 校验关系分类是否存在
    if node_id and not module_info:
        return utils.rander(utils.DATA_ERR, '无此父级关系分类')

    sort = models.Folder.query.filter_by(node_id=node_id).count()
    # 数据创建
    new_module = models.Folder(
        project_id=project_id,
        name=name,
        node_id=node_id,
        data_type=data_type,
        sort=sort + 1
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
    return utils.rander(utils.OK, data=items)


@api.route('/business/folder/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('folderDelete.yaml')
def delete_folder_info():
    """ 删除模块信息 """

    return utils.delete(models.Folder, dict(id='id'), dict(node_id='id'))


@api.route('/business/folder/move', methods=['POST', 'PUT'])
@utils.login_required
def move_folder_info():
    """ 移动文件夹位置 """
    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    folder_id = body.get('id')
    node_id = body.get('nodeId')
    position = body.get('position')  # 'before'、'inner'、'after'

    node = models.Folder.query.filter_by(id=node_id).first()
    folder = models.Folder.query.filter_by(id=folder_id)

    if not folder.first():
        return utils.rander(utils.DATA_ERR, '文件不存在')

    # 插入
    if position == 'inner':
        try:
            # 获取节点下的所有数据, 并修改此文件夹的排序信息
            children = models.Folder.query.filter_by(node_id=node.id)
            folder.update(dict(node_id=node_id, sort=children.count() + 1))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

    elif position == 'before':
        try:
            parent = models.Folder.query.filter(
                models.Folder.node_id == node.node_id,
                models.Folder.sort > node.sort
            ).all()
            print(parent, '11111')
            folder.update(dict(node_id=node.node_id, sort=node.sort))
            db.session.flush()
            for index, child in enumerate(parent):
                print(child.result, 111)
                print(node.sort + index + 1, 11111)
                child.update(dict(sort=node.sort + index + 1))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)
    else:
        try:
            parent = models.Folder.query.filter(
                models.Folder.node_id == node_id,
                models.Folder.sort > node.sort
            ).all()
            folder.update(dict(node_id=node.node_id, sort=node.sort + 1))
            for index, child in enumerate(parent):
                child.update(dict(sort=node.sort + index + 2))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
