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
        'flask-sqlalchemy',
        'flask',
        'redis',
        'flask-wtf',
        'pymysql',
        'flask_socketio',
        'eventlet',
        'authlib',
        'requests',
        'sqlalchemy',
        'click'
    ]
)
