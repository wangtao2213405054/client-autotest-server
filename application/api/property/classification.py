# _author: Coke
# _date: 2022/4/30 01:42

from flask import request
from application.api import api, swagger
from application import db, models, utils

import logging


@api.route('/account/classification/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('classificationEdit.yaml')
def edit_classification_info():
    """ 新增/修改关系分类 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    node_id = body.get('nodeId')
    name = body.get('name')
    classification_id = body.get('id')

    if not name:
        return utils.rander(utils.DATA_ERR, '名称不可为空')

    if not node_id:
        node_id = 0

    # 验证是否数据重复
    classification = models.Classification.query.filter_by(name=name, node_id=node_id).first()
    if classification and classification_id != classification.id:
        return utils.rander(utils.DATA_ERR, '名称不可重复')

    # 修改
    if classification_id:
        classification_info = models.Classification.query.filter_by(id=classification_id)
        if not classification_info.first():
            return utils.rander(utils.DATA_ERR, '此关系分类不存在')

        try:
            classification_info.update({'name': name})
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander(utils.DATABASE_ERR)
        return utils.rander(utils.OK)

    classification_info = models.Classification.query.filter_by(id=node_id).first()

    # 校验关系分类是否存在
    if node_id and not classification_info:
        return utils.rander(utils.DATA_ERR, '无此父级关系分类')

    # 创建关系分类深度校验
    if classification_info and classification_info.node_id != 0:
        return utils.rander(utils.DATA_ERR, '最多只允许创建二级关系分类')

    # 数据创建
    new_classification = models.Classification(
        name=name,
        node_id=node_id
    )

    # 处理数据库存储异常
    try:
        db.session.add(new_classification)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/account/classification/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('classificationList.yaml')
def get_classification_list():
    """ 获取关系分类列表tree """

    classification_list = models.Classification.query.filter_by(node_id=0).all()

    classification_dict_list = []

    # 循环所有一级tree
    for item in classification_list:

        father = item.result
        father['children'] = []

        # 获取所有当前一级tree下的子信息
        classification_son = models.Classification.query.filter_by(node_id=item.id).all()

        # 将二级tree添加至一级tree的children中
        for value in classification_son:
            father['children'].append(value.result)

        classification_dict_list.append(father)

    return utils.rander(utils.OK, data=classification_dict_list)


@api.route('/account/classification/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('classificationDelete.yaml')
def delete_classification_info():
    """ 删除关系分类 """

    return utils.delete(models.Classification, dict(id='id'), dict(node_id='id'))
