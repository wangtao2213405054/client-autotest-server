# _author: Coke
# _date: 2022/8/10 14:06

from flask import Blueprint


# 创建 Socket 蓝图对象
ws = Blueprint('socket_api', __name__)

# 内存变量
online_server = []
session_maps = {}  # session 映射 userId: session


def blueprint():
    # 导入蓝图视图
    from application.ws import connect
    from .system import system
    from .room import join, leave


blueprint()
