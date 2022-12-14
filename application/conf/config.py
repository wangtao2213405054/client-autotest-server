# _author: Coke
# _date: 2022/4/12 11:03

import logging
import os
import re


class Config:
    """ 配置信息 """

    # Token 密钥 和 有效时间
    TOKEN_SIGN_KEY = 'SL*JK%!@#*&(SAX!@LK((#$'
    TOKEN_TIME_LIMIT = 86400

    # CSRF 密钥
    SECRET_KEY = '4d456f5e604e47118dd8dd5d84c16f76'

    # Redis 数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 123456

    # Mysql 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 60  # 数据库超时时间

    # Log 路径
    OBJ_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
    LOG = os.path.join(OBJ_PATH, 'logs')
    if not os.path.exists(LOG):
        os.mkdir(LOG)
    LOG_PATH = os.path.join(LOG, 'log.log')
    # 日志大小
    LOG_BYTES = 1024 * 1024 * 100
    # 日志数量
    LOG_COUNT = 10

    API_URL_PREFIX = '/api/v1/client'
    SOCKET_URL_PREFIX = '/ws/v1/client'
    # 引擎映射
    SQLALCHEMY_BINDS = dict()


class LocalConfig(Config):
    """ 本地环境 """
    DEBUG = True
    # 日志等级
    LOGGING = logging.DEBUG

    # 显示 SQL 信息
    SQLALCHEMY_ECHO = False

    # Mysql 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456789@127.0.0.1:3306/TestPlatform'


class DevelopConfig(Config):
    """ 测试环境 """
    DEBUG = True
    # 日志等级
    LOGGING = logging.DEBUG

    # mysql 数据库
    # 创建表使用 admin_ddl 账号
    # 新增数据使用 develop 账号
    SQLALCHEMY_DATABASE_URI = ''


class ProductConfig(Config):
    """ 正式环境 """

    # 日志等级
    LOGGING = logging.INFO

    # Mysql 数据库
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False


# 配置文件映射
Config_Map = {
    "daily": DevelopConfig,
    "public": ProductConfig,
    "local": LocalConfig
}


def get_model_class(path, maps):
    """ 将 models 模块下的所有模型添加到 SQLALCHEMY_BINDS 映射中 """
    for item in os.listdir(path):
        _path = os.path.join(path, item)
        if os.path.isfile(_path):
            if '.py' in item and 'pyc' not in item and '__init__' not in item:
                with open(_path, 'r', encoding='utf-8') as file:
                    data = file.read()

                _compile = re.compile(r"__bind_key__ = '\w+")
                _bind_key = _compile.findall(data)
                for _class in _bind_key:
                    _bind = re.sub("__bind_key__ = '", '', _class)
                    maps.SQLALCHEMY_BINDS[_bind] = maps.SQLALCHEMY_DATABASE_URI

        else:
            get_model_class(os.path.join(path, item), maps)


for key, value in Config_Map.items():
    get_model_class(
        os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')),
        value
    )
