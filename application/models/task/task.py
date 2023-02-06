# _author: Coke
# _date: 2022/12/13 13:56

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db, models

import json


class Task(BaseModel, db.Model):
    """ 任务列表 """

    __bind_key__ = 'task'
    __tablename__ = 'test_client_task'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 任务名称
    platform = Column(db.String(64), nullable=False)  # 所属平台
    environmental = Column(db.Integer, nullable=False)  # 所属环境
    url = Column(db.Text, nullable=False)  # 安装包连接或启动连接
    cases = Column(db.Text, nullable=False)  # 要运行的 Case 列表
    username = Column(db.String(64))  # 创建人
    devices = Column(db.Integer)  # 指定的运行设备
    project_id = Column(db.Integer)  # 所属项目
    status = Column(db.Integer)  # 任务状态 0 待执行 1 执行中 2 执行成功 3 执行失败 4任务暂停
    sign = Column(db.Boolean)  # 任务标记, 为真时说明任务已经发放
    pass_case = Column(db.Integer)  # 成功用例数
    fail_case = Column(db.Integer)  # 失败用例数

    def __init__(self, name, platform, environmental, url, cases, username, project_id, devices=None):
        self.name = name
        self.platform = platform.lower()
        self.environmental = environmental
        self.url = url
        self.cases = json.dumps(cases)
        self.devices = devices
        self.username = username
        self.project_id = project_id
        self.status = 0
        self.sign = False
        self.pass_case = 0
        self.fail_case = 0

    @property
    def result(self):
        devices_name = models.Worker.query.filter_by(id=self.devices).first()
        return {
            'id': self.id,
            'name': self.name,
            'platform': self.platform,
            'environmental': self.environmental,
            'environmentalName': models.Domain.query.filter_by(id=self.environmental).first().name,
            'url': self.url,
            'cases': json.loads(self.cases),
            'devices': self.devices,
            'devicesName': devices_name.name if devices_name else '',
            'username': self.username,
            'projectId': self.project_id,
            'status': self.status,
            'count': len(json.loads(self.cases)),
            'passCase': self.pass_case,
            'failCase': self.fail_case,
            'percentage': round((self.pass_case + self.fail_case) / len(json.loads(self.cases)) * 100, 2),
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app('local')
    # get bing func:
    # flask-sqlalchemy => 3.0.0 db.engines.get(None)
    # flask-sqlalchemy < 3.0.0 db.session.bind
    with app.app_context():
        # db.drop_all('task')
        # db.create_all(Task.__bind_key__)
        Task.__table__.drop(db.engines.get(None))
        Task.__table__.create(db.engines.get(None))
