# _author: Coke
# _date: 2022/8/10 14:35

from application import create_app, socketio

build = 'daily'


app = create_app(build)


if __name__ == '__main__':
    socketio.run(app)
