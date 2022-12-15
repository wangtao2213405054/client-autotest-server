# _author: Coke
# _date: 2022/12/15 10:45

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db


class Version(BaseModel, db.Model):
    """ 任务列表 """

    __bind_key__ = 'version'
    __tablename__ = 'test_client_version'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 版本名称
    identify = Column(db.Integer, nullable=False)  # 版本标识符
    project_id = Column(db.Integer, nullable=False)  # 所属项目
    desc = Column(db.Text)  # 版本描述

    def __init__(self, name, identify, project_id, desc):
        self.name = name
        self.identify = identify
        self.project_id = project_id
        self.desc = desc

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'identify': self.identify,
            'project_id': self.project_id,
            'desc': self.desc,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app('local')
    # get bing func:
    # flask-sqlalchemy => 3.0.0 db.engines.get(None)
    # flask-sqlalchemy < 3.0.0 db.session.bind
    with app.app_context():
        # db.drop_all(Version.__bind_key__)
        # db.create_all(Version.__bind_key__)
        Version.__table__.drop(db.engines.get(None))
        Version.__table__.create(db.engines.get(None))
