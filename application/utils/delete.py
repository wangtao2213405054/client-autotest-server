# _author: Coke
# _date: 2022/8/23 14:52

from application import utils, db
from flask import request
from sqlalchemy import or_

import logging


def delete(_models, _request: dict, children: dict = None):
    """
    封装的通用删除
    :param _models: 要删除的数据所在表
    :param _request: 要从 request 中获取的数据 { 'domain_id': 'id' }, key对应数据库, value 对应request中的值
    :param children: 是否包含子节点 如何为真则填写其数据库字段
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    _request_list = []
    filter_by = {}

    for key, value in _request.items():
        _param = body.get(value)
        _request_list.append(_param)
        filter_by[key] = _param

    if not all(_request_list):
        return utils.rander(utils.DATA_ERR)

    delete_info = _models.query.filter_by(**filter_by)

    if not delete_info.first():
        return utils.rander(utils.DATA_ERR, '数据不存在')

    try:
        if children:
            for key, value in children.items():
                children[key] = body.get(value)
            _models.query.filter_by(**children).delete()
        delete_info.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


def delete_or(_models, condition, _list):
    """
    以或的关系删除数据
    :param _models: 数据表
    :param condition: 条件
    :param _list: 要删除的数据组
    :return:
    """
    try:
        _models.query.filter(or_(*[condition == item for item in _list])).delete()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
