# _author: Coke
# _date: 2022/11/18 15:26

from application import socketio, utils
from application.api import api

import time


task_list = [{'taskId': index, 'taskName': f'{index}'} for index in range(100)]
lock = False


@api.route('/task/get', methods=['GET'])
def task_dispenser():
    """
    分配任务给客户端
    :return:
    """

    _task = {}
    if len(task_list):
        _task = task_list[0]
        del task_list[0]

    return utils.rander('OK', data=_task)
