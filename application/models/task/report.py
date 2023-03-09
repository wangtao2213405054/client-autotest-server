# _author: Coke
# _date: 2022/12/14 14:19

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db
from sqlalchemy.dialects.mysql import LONGTEXT

import json


class Report(BaseModel, db.Model):
    """ 测试报告表 """

    __bind_key__ = 'report'
    __tablename__ = 'test_client_report'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 报告名称
    task_id = Column(db.Integer, nullable=False)  # 所属任务
    status = Column(db.Integer, nullable=False)  # 报告状态 0 成功 1 成功 2 失败 3 异常
    case_id = Column(db.Integer, nullable=False)  # 用例 ID
    details = Column(db.Text)  # 报告描述
    module = Column(db.String(32), nullable=False)  # 所属模块
    set_list = Column(db.Text, nullable=False)  # 集合列表
    priority = Column(db.String(32), nullable=False)  # 用例优先级
    output = Column(LONGTEXT)  # 运行日志
    images = Column(db.Text)  # 图片列表
    error_step = Column(db.Text)  # 错误步骤
    error_info = Column(db.Text)  # 错误信息
    error_details = Column(db.Text)  # 错误详情
    gif = Column(db.Text)  # Gif 图片
    start_time = Column(db.String(32), nullable=False)  # 开始时间
    stop_time = Column(db.String(32), nullable=False)  # 结束时间
    duration = Column(db.Float, nullable=False)  # 运行时长

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.task_id = kwargs.pop('task_id')
        self.status = kwargs.pop('status')
        self.case_id = kwargs.pop('case_id')
        self.details = kwargs.pop('details')
        self.module = kwargs.pop('module')
        self.set_list = json.dumps(kwargs.pop('set_list'), ensure_ascii=False)
        self.priority = kwargs.pop('priority')
        self.output = kwargs.pop('output')
        self.images = json.dumps(kwargs.pop('images'), ensure_ascii=False)
        self.error_step = kwargs.pop('error_step')
        self.error_info = kwargs.pop('error_info')
        self.error_details = kwargs.pop('error_details')
        self.gif = kwargs.pop('gif')
        self.start_time = kwargs.pop('start_time')
        self.stop_time = kwargs.pop('stop_time')
        self.duration = kwargs.pop('duration')

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            taskId=self.task_id,
            status=self.status,
            caseId=self.case_id,
            details=self.details,
            module=self.module,
            setList=json.loads(self.set_list),
            priority=self.priority,
            output=self.output,
            images=json.loads(self.images),
            errorStep=self.error_step,
            errorInfo=self.error_info,
            errorDetails=self.error_details,
            gif=self.gif,
            startTime=self.start_time,
            stopTime=self.stop_time,
            duration=self.duration
        )


if __name__ == '__main__':
    app = create_app('local')
    # get bing func:
    # flask-sqlalchemy => 3.0.0 db.engines.get(None)
    # flask-sqlalchemy < 3.0.0 db.session.bind
    with app.app_context():
        Report.__table__.drop(db.engines.get(None))
        Report.__table__.create(db.engines.get(None))
