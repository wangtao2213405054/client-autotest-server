# _author: Coke
# _date: 2022/8/23 14:00


def paginate(model, page, size, filter_list: list = None, filter_by: dict = None, order_by=True):
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

    if filter_list is None:
        filter_list = []

    if filter_by is None:
        filter_by = {}

    models = model.query.filter(*filter_list).filter_by(**filter_by).order_by(
        model.id.desc() if order_by else None
    )
    models_list = models.paginate(page, size, False).items
    total = models.count()
    return models_list, total
