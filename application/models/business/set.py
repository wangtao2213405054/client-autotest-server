# _author: Coke
# _date: 2022/12/15 11:09


from application.models.base import BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT
from application import create_app, db

import json


class Set(BaseModel, db.Model):
    """ 任务列表 """

    __bind_key__ = 'set'
    __tablename__ = 'test_client_set'
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False)  # 集合名称
    special = Column(db.Boolean, nullable=False)  # 是否为自定义集合
    project_id = Column(db.Integer, nullable=False)  # 所属项目
    desc = Column(db.Text)  # 版本描述
    custom_set = Column(LONGTEXT)  # 测试用例集
    case_list = Column(LONGTEXT)  # 测试用例id集合

    def __init__(self, name, special, project_id, desc, custom_set, case_list):
        self.name = name
        self.special = special
        self.project_id = project_id
        self.desc = desc
        self.custom_set = json.dumps(custom_set, ensure_ascii=False)
        self.case_list = json.dumps(case_list, ensure_ascii=False)

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'special': self.special,
            'project_id': self.project_id,
            'customSet': json.loads(self.custom_set),
            'caseList': json.loads(self.case_list),
            'desc': self.desc,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        # Set.__table__.drop(db.engines.get(None))
        Set.__table__.create(db.engines.get(None))
