# _author: Coke
# _date: 2022/12/16 22:50

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db
from sqlalchemy.dialects.mysql import LONGTEXT

import json


class Case(BaseModel, db.Model):
    """ 任务列表 """

    __bind_key__ = 'case'
    __tablename__ = 'test_client_case'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 版本名称
    desc = Column(db.Text)  # 版本描述
    special = Column(db.Boolean, nullable=False)  # 特殊用例
    action = Column(db.Boolean, nullable=False)  # 是否执行
    start_version = Column(db.Integer)  # 开始版本
    end_version = Column(db.Integer)  # 结束版本
    set_info = Column(db.Text, nullable=False)  # 集合信息
    platform = Column(db.Text, nullable=False)  # 所属平台
    priority = Column(db.Integer, nullable=False)  # 优先级
    officer_list = Column(db.Text, nullable=False)  # 责任人
    module = Column(db.Integer, nullable=False)  # 所属模块
    business = Column(db.Integer, nullable=False)  # 所属业务
    case_steps = Column(LONGTEXT, nullable=False)  # 测试步骤
    create_id = Column(db.Integer, nullable=False)  # 创建人ID
    update_id = Column(db.Integer, nullable=False)  # 修改人ID
    project_id = Column(db.Integer, nullable=False)  # 项目ID
    pre_position = Column(db.Text)  # 前置用例
    post_position = Column(db.Text)  # 后置用例

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.desc = kwargs.pop('desc', None)
        self.special = kwargs.pop('special')
        self.action = kwargs.pop('action')
        self.start_version = kwargs.pop('start_version')
        self.end_version = kwargs.pop('end_version')
        self.set_info = json.dumps(kwargs.pop('set_info'))
        self.platform = json.dumps(kwargs.pop('platform'))
        self.priority = kwargs.pop('priority')
        self.officer_list = json.dumps(kwargs.pop('officer_list'))
        self.module = kwargs.pop('module')
        self.business = kwargs.pop('business')
        self.case_steps = json.dumps(kwargs.pop('case_steps'), ensure_ascii=False)
        self.create_id = kwargs.pop('create_id')
        self.update_id = kwargs.pop('update_id')
        self.project_id = kwargs.pop('project_id')
        self.pre_position = json.dumps(kwargs.pop('pre_position'))
        self.post_position = json.dumps(kwargs.pop('post_position'))

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'special': self.special,
            'action': self.action,
            'startVersion': self.start_version,
            'endVersion': self.end_version,
            'setInfo': json.loads(self.set_info),
            'platform': json.loads(self.platform),
            'priority': self.priority,
            'officerList': json.loads(self.officer_list),
            'createId': self.create_id,
            'updateId': self.update_id,
            'moduleList': [self.business, self.module],
            'prePosition': json.loads(self.pre_position),
            'postPosition': json.loads(self.post_position),
            'projectId': self.project_id,
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
        Case.__table__.drop(db.engines.get(None))
        Case.__table__.create(db.engines.get(None))
