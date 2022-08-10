# _author: Coke
# _date: 2022/4/12 11:37

from application import socketio
from flask import request
from application.ws import online_server

import logging


@socketio.on('disconnect')
def test_disconnect():
    """ 销毁钩子 """

    header = request.headers
    server_name = header.get('name')

    if server_name and server_name in online_server:
        online_server.remove(server_name)

    logging.info(f'{server_name} offline')
    socketio.emit('property count', f'{server_name}已下线')
