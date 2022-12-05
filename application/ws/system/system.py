# _author: Coke
# _date: 2022/9/28 16:39

from application import socketio
from flask_socketio import join_room, close_room
from flask import request


@socketio.on('system')
def get_system_info(data):
    """ 将获取到的系统信息分发到指定的房间之中 """
    socketio.emit('clientSystemInfo', data, room=f'systemRoom{getattr(request, "sid", None)}')
