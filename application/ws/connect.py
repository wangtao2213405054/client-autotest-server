# _author: Coke
# _date: 2022/4/12 11:11

from application import socketio, utils
from flask import request
from application.ws import online_server, session_maps


import logging


@socketio.on('connect')
def connect():
    """ 挂载钩子 """

    header = request.headers

    # 获取启动的标记符并将其存储在内存中
    device_token = header.get('token')

    if not device_token:
        logging.info('socket no token')
        return False

    payload = utils.analytic_token(device_token)
    if not payload.get('results'):
        return False

    user_info = payload.get('info')
    user_id, username = user_info.get('user_id'), user_info.get('username')

    if user_id not in online_server:
        online_server.append(user_id)

    # 将 session id 更新
    session_maps[user_id] = getattr(request, 'sid', None)

    logging.info(f'{username} online')

    if isinstance(user_id, str):
        master = utils.get_master_info(user_id)
        if master:
            socketio.emit('masterOnline', {'id': master.id, 'online': True})


@socketio.on('disconnect')
def test_disconnect():
    """ 销毁钩子 """

    header = request.headers
    device_token = header.get('token')

    payload = utils.analytic_token(device_token)

    user_info = payload.get('info')
    user_id, username = user_info.get('user_id'), user_info.get('username')

    if user_id in online_server:
        online_server.remove(user_id)

    if user_id in session_maps:
        del session_maps[user_id]

    logging.info(f'{username} offline')

    if isinstance(user_id, str):
        master = utils.get_master_info(user_id)
        if master:
            socketio.emit('masterOnline', {'id': master.id, 'online': False})
