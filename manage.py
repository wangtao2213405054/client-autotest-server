# _author: Coke
# _date: 2022/8/10 14:35

from application import create_app, socketio

import json

build = 'local'
app = create_app(build)


@app.errorhandler(404)
def handle_error(e):
    """ 封装错误日志 """
    # logging.error(e)
    # print(e)
    return json.dumps({'test': 123})


if __name__ == '__main__':
    # _system = importlib.import_module('application.ws.system.system')
    # app.before_first_request(_system.thread_test)
    socketio.run(app)
