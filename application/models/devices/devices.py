# _author: Coke
# _date: 2022/11/28 11:39

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db

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
    log = Column(db.String(32), nullable=False)  # 日志等级

    def __init__(self, name, token, max_context, key, desc, role, log, project_id=None, status=True, context=0):
        self.name = name
        self.token = token
        self.max_context = max_context
        self.log = log
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
            'logging': self.log,
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
    mapping = db.Column(db.TEXT, nullable=False)  # map 映射
    status = db.Column(db.Integer, nullable=False)  # 设备状态 0空闲 1任务中 2异常 3 停止 4 离线
    cause = db.Column(db.TEXT)  # 导致异常或失败的原因, 最近一次
    switch = db.Column(db.Boolean, nullable=False)  # 是否执行任务
    actual = db.Column(db.Integer, nullable=False)  # 成功执行任务的次数
    master = db.Column(db.Integer, nullable=False)  # 隶属于控制器的ID
    blocker = db.Column(db.Integer, nullable=False)  # 阻断器，当连续失败次数达到后将此设备变为异常
    log = Column(db.String(32), nullable=False)  # 日志等级

    def __init__(self, name, desc, mapping, master, blocker, switch, log):
        self.name = name
        self.key = uuid.uuid1().hex
        self.desc = desc
        self.mapping = json.dumps(mapping, ensure_ascii=False)
        self.status = 0
        self.actual = 0
        self.switch = switch
        self.master = master
        self.blocker = blocker
        self.log = log

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'desc': self.desc,
            'mapping': self.mapping,
            'status': self.status,
            'cause': self.cause,
            'actual': self.actual,
            'master': self.master,
            'blocker': self.blocker,
            'switch': self.switch,
            'logging': self.log,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        db.drop_all(Master.__bind_key__)
        db.create_all(Master.__bind_key__)
