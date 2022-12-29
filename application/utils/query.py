# _author: Coke
# _date: 2022/8/23 14:00

from application import models
from flask import request

import logging


def paginate(model, page, size, filter_list: list = None, filter_by: dict = None, order_by=True, **kwargs):
    """
    获取数据分页
    :param model: 数据对象
    :param page: 页码
    :param size: 每页大小
    :param filter_list: 过滤器 filter
    :param filter_by: 过滤器 filter_by
    :param order_by: 是否倒序
    :return:
    """

    source = kwargs.pop('source', True)

    if filter_list is None:
        filter_list = []

    if filter_by is None:
        filter_by = {}

    _models = model.query.filter(*filter_list).filter_by(**filter_by).order_by(
        model.id.desc() if order_by else None
    )

    # 修复 flask-sqlalchemy 3.0.2 版本传参问题
    models_list = list(map(
        lambda x: x.result if source else x,
        _models.paginate(page=page, per_page=size, error_out=False).items
    ))
    total = _models.count()
    return models_list, total


def get_master_info(key):
    """ 获取通过 Key 控制设备信息 """

    try:
        master = models.Master.query.filter_by(key=key).first()
        return master
    except Exception as e:
        logging.error(e)


def query_id():
    """ 从 request 中获取 id """
    body = request.get_json()

    if not body:
        return False

    _id = body.get('id')

    return _id
