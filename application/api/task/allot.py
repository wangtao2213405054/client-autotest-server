# _author: Coke
# _date: 2022/11/18 15:26

from application import socketio, utils
from application.api import api

import random
import time

lock = utils.Lock()

task_list = [{
    'taskId': index,
    'taskName': f'{index}',
    'platform': random.choice(['ios', 'android'])
} for index in range(100)]


@api.route('/task/get', methods=['GET'])
def task_dispenser():
    """
    分配任务给客户端
    :return:
    """

    lock.acquire()

    _task = {}
    if len(task_list):
        _task = task_list[0]
        del task_list[0]

    time.sleep(2)

    lock.release()

    return utils.rander('OK', data={'free': True if _task else False, 'task': _task})
