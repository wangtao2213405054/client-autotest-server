# _author: Coke
# _date: 2022/8/10 18:12

import click
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@click.command()
@click.option('--port', '-p', default=5000, help='这是你要启动 Flask 服务器的端口号,默认5000')
@click.option('--host', '-h', default='127.0.0.1', help='这是你要启动 Flask 服务器的主机, 默认127.0.0.1')
@click.option('--env', '-e', default='public', help='启动 Flask 服务的环境, 默认public环境')
def flash(port, host, env):
    """
    启动服务器方法
    -.- 因为我没有找到给 create_app 传递参数的方法, 所以自己封装了一个命令行
    flask run ...
    :param port: 端口号
    :param host: 主机地址
    :param env: 环境
    :return:
    """
    from application import create_app, socketio
    app = create_app(env)
    socketio.run(app, host, port)


if __name__ == '__main__':
    flash()
