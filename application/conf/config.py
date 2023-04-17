# _author: Coke
# _date: 2022/4/12 11:03

from flasgger import Swagger

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

    # OSS 文件存储 本存储使用的是腾讯云的对象存储OSS服务
    # 上传文件接口在 api/upload/file 文件中, 如需修改其他服务请自行修改
    OSS_DICT = dict(
        Region='ap-beijing',
        SecretId='AKIDqSoxrSeSr1g4C4r2rQ7axmTitzufuk5I',
        SecretKey='42pY1H8l8NXZRBmCLRN9gxynjEVWcscE',
        Bucket='flash-1254275723'
    )

    # socket 域名信息
    SOCKET_HOST = 'http://127.0.0.1:5000'

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

    # Swagger
    SWAGGER = dict(
        title='客户端自动化平台接口',
        version='1.0.0',
        uiversion=3
    )
    SWAGGER_CONFIG = Swagger.DEFAULT_CONFIG
    SWAGGER_CONFIG['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
    SWAGGER_CONFIG['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
    SWAGGER_CONFIG['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
    SWAGGER_CONFIG['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
    SWAGGER_TEMPLATE = dict(securityDefinitions=dict(APIKeyHeader={
        'type': 'apiKey',
        'name': 'Token',
        'in': 'header'
    }))
    SWAGGER_CONFIG['specs_route'] = '/apidocs/'
    JSON_AS_ASCII = False


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

    # socket 域名信息
    SOCKET_HOST = 'http://gclcoke.online'


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
