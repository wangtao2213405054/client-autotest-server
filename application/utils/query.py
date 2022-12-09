# _author: Coke
# _date: 2022/8/23 14:00

from application import models

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

    models = model.query.filter(*filter_list).filter_by(**filter_by).order_by(
        model.id.desc() if order_by else None
    )
    models_list = list(map(lambda x: x.to_dict if source else x, models.paginate(page, size, False).items))
    total = models.count()
    return models_list, total


def get_master_info(key):
    """ 获取通过 Key 控制设备信息 """

    try:
        master = models.Master.query.filter_by(key=key).first()
        return master
    except Exception as e:
        logging.error(e)
