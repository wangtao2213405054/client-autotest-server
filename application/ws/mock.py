# _author: Coke
# _date: 2023/8/27 21:01

from application import socketio, utils
from flask import request

import re


@socketio.on('getMockData')
def mock_data(body: dict):
    """ 通过表达式信息, 获取需要随机的数据 """

    expression = body.get('expression')

    session_id = getattr(request, 'sid', None)

    socketio.emit('reverseMockData', str(utils.decouple(expression)), to=session_id)


@socketio.on('transitionStringData')
def transition_string_data(data: str):
    """ 将字符串中带有模拟的数据转换 """

    for item in re.findall(r"{{.*?}}", data):
        data = data.replace(item, str(utils.decouple(item)))

    session_id = getattr(request, 'sid', None)
    socketio.emit('previewString', data, to=session_id)
