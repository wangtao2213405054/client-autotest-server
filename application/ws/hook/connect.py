# _author: Coke
# _date: 2022/4/12 11:11

from application import socketio
from flask import request
from application.ws import online_server

import logging


@socketio.on('connect')
def connect():
    """ 挂载钩子 """

    header = request.headers

    # 获取启动的标记符并将其存储在内存中
    server_name = header.get('name')

    if server_name and server_name not in online_server:
        online_server.append(server_name)

    logging.info(f'{server_name} online')
    socketio.emit('property count', f'{server_name}已上线')
