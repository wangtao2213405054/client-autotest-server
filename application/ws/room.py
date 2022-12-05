# _author: Coke
# _date: 2022/9/29 14:00

from application import socketio
from flask_socketio import join_room, leave_room, rooms

"""
bug record: 一定要确保加入房间和退出房间是真实存在的，如果不存在则会出现问题
"""


@socketio.on('joinRoom')
def join_rooms(body):
    """ 加入指定房间 """
    room = body.get('roomId')
    if room and room not in rooms():
        join_room(room)


@socketio.on('leaveRoom')
def leave_rooms(body):
    """ 退出指定房间 """
    room = body.get('roomId')
    if room and room in rooms():
        leave_room(room)
