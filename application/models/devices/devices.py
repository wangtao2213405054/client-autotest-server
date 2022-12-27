# _author: Coke
# _date: 2022/11/28 11:39

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db
from sqlalchemy.dialects.mysql import LONGTEXT

import json
import uuid


class Master(BaseModel, db.Model):
    """ 控制设备信息表 """

    __bind_key__ = 'master'
    __tablename__ = 'test_client_device_master'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 设备名称
    token = Column(db.TEXT, nullable=False)  # 令牌
    key = Column(db.String(64), nullable=False, unique=True)  # 设备唯一标识符
    desc = db.Column(db.Text)  # 设备描述信息
    role = Column(db.Integer, nullable=False)  # 角色
    status = Column(db.Boolean, nullable=False)  # 设备状态
    context = Column(db.Integer)  # 已绑定的设备数
    max_context = Column(db.Integer, nullable=False)  # 最大设备绑定数
    project_id = Column(db.Integer)  # 所属项目ID

    def __init__(self, name, token, max_context, key, desc, role, project_id=None, status=True, context=0):
        self.name = name
        self.token = token
        self.max_context = max_context
        self.key = key
        self.desc = desc
        self.role = role
        self.status = status
        self.project_id = project_id
        self.context = context

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'token': self.token,
            'maxContext': self.max_context,
            'desc': self.desc,
            'role': self.role,
            'status': self.status,
            'projectId': self.project_id,
            'context': self.context,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class Worker(BaseModel, db.Model):
    """ 执行设备信息表 """

    __bind_key__ = 'worker'
    __tablename__ = 'test_client_device_worker'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    key = Column(db.String(64), nullable=False, unique=True)  # 设备唯一标识符
    name = Column(db.String(32), nullable=False)  # 设备名称
    desc = db.Column(db.TEXT)  # 设备描述信息
    platform = db.Column(db.String(32), nullable=False)  # 所属平台
    mapping = db.Column(db.TEXT, nullable=False)  # map 映射
    parsing = db.Column(db.TEXT, nullable=False)  # 解析后的映射
    status = db.Column(db.Integer, nullable=False)  # 设备状态 0空闲 1任务中 2异常 3 停止 4 离线
    cause = db.Column(db.TEXT)  # 导致异常或失败的原因, 最近一次
    switch = db.Column(db.Boolean, nullable=False)  # 是否执行任务
    actual = db.Column(db.Integer, nullable=False)  # 成功执行任务的次数
    master = db.Column(db.Integer, nullable=False)  # 隶属于控制器的ID
    blocker = db.Column(db.Integer, nullable=False)  # 阻断器，当连续失败次数达到后将此设备变为异常

    def __init__(self, name, desc, platform, mapping, parsing, master, blocker, switch):
        self.name = name
        self.key = uuid.uuid1().hex
        self.desc = desc
        self.platform = platform
        self.mapping = json.dumps(mapping, ensure_ascii=False)
        self.parsing = json.dumps(parsing, ensure_ascii=False)
        self.status = 0
        self.actual = 0
        self.switch = switch
        self.master = master
        self.blocker = blocker

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'desc': self.desc,
            'platformName': self.platform,
            'mapping': json.loads(self.mapping),
            'parsing': json.loads(self.parsing),
            'status': self.status,
            'cause': self.cause,
            'actual': self.actual,
            'master': self.master,
            'blocker': self.blocker,
            'switch': self.switch,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class Capabilities(BaseModel, db.Model):
    """ 执行设备信息表 """

    __bind_key__ = 'capabilities'
    __tablename__ = 'test_client_device_capabilities'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 设备名称
    platform_name = Column(db.String(64), nullable=False)  # 平台映射
    mapping = Column(LONGTEXT, nullable=False)  # 映射列表

    def __init__(self, name, platform_name, mapping):
        self.name = name
        self.platform_name = platform_name
        self.mapping = json.dumps(mapping, ensure_ascii=False)

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'platformName': self.platform_name,
            'mapping': json.loads(self.mapping),
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        db.drop_all(Capabilities.__bind_key__)
        db.create_all(Capabilities.__bind_key__)
