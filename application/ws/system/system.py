# _author: Coke
# _date: 2022/9/28 16:39

from application import socketio
from application.ws import session_maps

import random


@socketio.on('system')
def get_system_info(data):
    socketio.emit('returnSystem', data, room='Windows')


@socketio.on('test')
def thread_test():
    socketio.start_background_task(target=background_thread)


def background_thread():
    while True:
        socketio.sleep(5)
        t = random.randint(1, 100)
        print('running')
        socketio.emit('test', {'data': t}, room=session_maps.get(1))