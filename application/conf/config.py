# _author: Coke
# _date: 2022/4/12 11:03

import logging
import os


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
