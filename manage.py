# _author: Coke
# _date: 2022/8/10 14:35

from application import create_app, socketio

build = 'local'


app = create_app(build)


if __name__ == '__main__':
    # _system = importlib.import_module('application.ws.system.system')
    # app.before_first_request(_system.thread_test)
    socketio.run(app)
