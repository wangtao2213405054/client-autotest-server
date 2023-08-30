# _author: Coke
# _date: 2022/8/10 14:05

from flask import Blueprint
from flasgger import swag_from

import traceback
import os

# 创建蓝图对象
api = Blueprint('app_api', __name__)


def swagger(swagger_name):
    """
    重写了 swag_from 方法
    :param swagger_name: swagger 文件名称 .yaml 文件
    请在 application/api/swagger 目录下查看接口文档
    此方法依赖于目录结构, 请勿修改 api 环境下的目录结构
    """

    result = traceback.extract_stack()
    caller = result[len(result) - 2]
    # 获取调用函数的模块文件绝对路径
    callback = str(caller).split(',')[0].lstrip('<FrameSummary file ')
    # 获取调用函数所在的父级目录
    father_caller = os.path.basename(os.path.dirname(callback))
    swagger_path = os.path.join(os.path.dirname(__file__), 'swagger', father_caller, swagger_name)
    return swag_from(swagger_path)


def blueprint():
    # 导入蓝图视图

    from .property import authentication, classification, management
    from .permissions import menu, role
    from .business import project, folder, set, version, case
    from .conf import email, robot, element, event, socket, dictionary, dynamic
    from .task import allot, center, report
    from .devices import master, worker
    from .message import message
    from .mock import domain, api
    from .upload import file


blueprint()
