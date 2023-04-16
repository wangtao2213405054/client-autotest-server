# _author: Coke
# _date: 2022/8/10 14:02

from setuptools import find_packages, setup

setup(
    name='application',
    description='this is the client autotest platform server',
    url='https://github.com/wangtao2213405054/client-autotest-server',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask-sqlalchemy >= 3.0.0',
        'flask >= 2.2.2',
        'redis',
        'flask-wtf',
        'cos-python-sdk-v5',  # 腾讯云OSS 系统存储桶, 可根据实际项目替换为对应的存储系统
        'pymysql',
        'flask_socketio >= 5.3.2',
        'eventlet',
        'authlib',
        'requests',
        'pypinyin',
        'python-socketio >= 5.7.2',
        'sqlalchemy >= 1.4.45',
        'click',
        'flasgger >=0.9.5'
    ]
)
