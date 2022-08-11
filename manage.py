# _author: Coke
# _date: 2022/8/10 14:35

from application import create_app, socketio

build = 'local'


app = create_app(build)


@app.errorhandler(500)
def handle_error(e):
    """ 封装错误日志 """
    print('2221231232131')
    return '服务器搬家了'


if __name__ == '__main__':
    socketio.run(app)
