# _author: Coke
# _date: 2022/8/10 14:01


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from .conf.config import Config_Map
from logging.handlers import RotatingFileHandler
# from flask_wtf.csrf import CSRFProtect

import redis
import pymysql
import logging
import sys


# Mysql 数据库连接
db = SQLAlchemy()

# Redis 数据库连接
rd = None

# token 全局变量
TOKEN_SIGN_KEY = None
TOKEN_TIME_LIMIT = None
accessKey = None

# Socket 连接
socketio = SocketIO(cors_allowed_origins='*')

# url 前缀
API_URL_PREFIX = ''
SOCKET_URL_PREFIX = ''


def create_app(config: str):
    """
    创建 flask 对象
    :param config: 配置模式名称 daily or public
    :return: 返回 flask 对象
    """
    # print(config.__dict__, '123321')
    app = Flask(__name__)

    # 根据工厂模式获取配置文件映射
    config_class = Config_Map.get(config)
    app.config.from_object(config_class)

    # 初始化 Mysql 数据库
    pymysql.install_as_MySQLdb()
    db.init_app(app)

    # 初始化 Redis 数据库
    global rd
    rd = redis.Redis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, password=config_class.REDIS_PASSWORD)

    # 定义 Token
    global TOKEN_SIGN_KEY, TOKEN_TIME_LIMIT, accessKey, API_URL_PREFIX, SOCKET_URL_PREFIX
    TOKEN_SIGN_KEY, TOKEN_TIME_LIMIT = config_class.TOKEN_SIGN_KEY, config_class.TOKEN_TIME_LIMIT
    API_URL_PREFIX, SOCKET_URL_PREFIX = config_class.API_URL_PREFIX, config_class.SOCKET_URL_PREFIX

    # 补充 csrf 防护
    # CSRFProtect(app)

    # 注册蓝图
    from application import ws
    from application import api
    app.register_blueprint(api.api, url_prefix=API_URL_PREFIX)
    app.register_blueprint(ws.ws, url_prefix=SOCKET_URL_PREFIX)

    # 创建日志记录器 指定Log路径 指定日志大小 指定保留几个日志文件 读取配置文件
    file_log_handler = RotatingFileHandler(config_class.LOG_PATH, maxBytes=config_class.LOG_BYTES,
                                           backupCount=config_class.LOG_COUNT, encoding='utf-8')
    # 为刚创建的日志记录器设置日志记录格式
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    file_log_handler.setFormatter(formatter)

    # 设置输出流样式及等级
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    logging.basicConfig(level=config_class.LOGGING, handlers=[handler])

    # 添加全局日志工具对象
    logging.getLogger().addHandler(file_log_handler)

    # 注册 Socket
    socketio.init_app(app)

    return app
