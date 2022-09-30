# _author: Coke
# _date: 2022/9/29 14:00

from application import socketio
from flask_socketio import join_room, leave_room


@socketio.on('joinRoom')
def join(body):
    """ 加入指定房间 """
    join_room(body.get('roomId'))


@socketio.on('leaveRoom')
def leave(body):
    """ 退出指定房间 """
    leave_room(body.get('roomId'))

