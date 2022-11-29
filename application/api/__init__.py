# _author: Coke
# _date: 2022/8/10 14:05

from flask import Blueprint

import logging


# 创建蓝图对象
api = Blueprint('app_api', __name__)


@api.errorhandler(500)
def handle_error(e):
    """ 封装错误日志 """
    logging.error(e)
    return '服务器搬家了'


def blueprint():
    # 导入蓝图视图

    from .property import authentication, classification, management
    from .permissions import menu, role
    from .business import project, folder
    from .conf import email, robot, element, event
    from .task import allot
    from .devices import master, worker, capabilities


blueprint()
