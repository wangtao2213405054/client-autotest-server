# _author: Coke
# _date: 2022/12/13 13:56

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db


class Task(BaseModel, db.Model):
    """ 任务列表 """

    __tablename__ = 'test_client_task'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 任务名称
    platform = Column(db.String(64), nullable=False)  # 所属平台
    version = Column(db.String(64))  # 运行版本
    devices = Column(db.Integer)  # 指定的运行设备
    project_id = Column(db.Integer)  # 所属项目
    status = Column(db.Integer)  # 任务状态 0 待执行 1 执行中 2 执行成功 3 执行失败

    def __init__(self, name, platform, version, project_id, devices=None):
        self.name = name
        self.platform = platform.lower()
        self.version = version
        self.devices = devices
        self.project_id = project_id
        self.status = 0

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'platform': self.platform,
            'version': self.version,
            'devices': self.devices,
            'projectId': self.project_id,
            'status': self.status,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        print(db.session.bind)
        Task.__table__.drop(db.session.bind)
        Task.__table__.create(db.session.bind)
