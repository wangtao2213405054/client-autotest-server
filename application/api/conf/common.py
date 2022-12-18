# _author: Coke
# _date: 2022/8/17 18:06

from application import utils, db

import logging


def message_switch(key, update, message, model):
    """
    更新开关状态
    :param key: id
    :param update: 要更新的信息
    :param message: 数据不存在的提示
    :param model: 模型表
    :return:
    """
    try:
        models = model.query.filter_by(id=key)
        if not models.first():
            return utils.rander(utils.DATA_ERR, message)
        models.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
