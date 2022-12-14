# _author: Coke
# _date: 2022/8/31 10:39

from application.models.base import BaseModel, db
from sqlalchemy.dialects.mysql import LONGTEXT
from application import create_app

import json


class Event(BaseModel, db.Model):
    """ 操作事件表 """

    __bind_key__ = 'event'
    __tablename__ = 'test_client_event'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)  # 事件名称
    mapping = db.Column(db.String(64), nullable=False)  # python函数映射
    platform = db.Column(db.String(64), nullable=False)  # 所属平台
    project_id = db.Column(db.Integer, nullable=False)  # 所属项目
    subset = db.Column(db.Boolean, nullable=False)  # 是否存在子集
    screenshot = db.Column(db.Boolean, nullable=False)  # 是否截图
    desc = db.Column(db.Text)  # 事件描述
    params = db.Column(LONGTEXT)  # 事件详细步骤参数

    def __init__(self, name, mapping, platform, project_id, desc, params, subset=False, screenshot=False):
        self.name = name
        self.mapping = mapping
        self.platform = platform
        self.project_id = project_id
        self.desc = desc
        self.params = json.dumps(params, ensure_ascii=False)
        self.subset = subset
        self.screenshot = screenshot

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            desc=self.desc,
            platform=self.platform,
            projectId=self.project_id,
            func=json.loads(self.params),
            mapping=self.mapping,
            subset=self.subset,
            screenshot=self.screenshot,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(Event.__bind_key__)
        db.create_all(Event.__bind_key__)
