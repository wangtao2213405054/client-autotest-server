# _author: Coke
# _date: 2022/12/14 14:19

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db


class Report(BaseModel, db.Model):
    """ 测试报告表 """

    __bind_key__ = 'report'
    __tablename__ = 'test_client_report'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 报告名称
    desc = Column(db.Text)  # 报告描述
    task_id = Column(db.Integer, nullable=False)  # 所属任务
    status = Column(db.Integer, nullable=False)  # 报告状态 0 成功 1 成功 2 失败 3 异常

    def __init__(self, name, desc, task_id, status):
        self.name = name
        self.desc = desc
        self.task_id = task_id
        self.status = status

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'taskId': self.task_id,
            'status': self.status,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app('local')
    # get bing func:
    # flask-sqlalchemy => 3.0.0 db.engines.get(None)
    # flask-sqlalchemy < 3.0.0 db.session.bind
    with app.app_context():
        Report.__table__.drop(db.engines.get(None))
        Report.__table__.create(db.engines.get(None))
