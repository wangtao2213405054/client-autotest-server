# _author: Coke
# _date: 2022/8/31 10:39

from application.models.base import BaseModel, db
from sqlalchemy.dialects.mysql import LONGTEXT
from application import create_app

import json


class Event(BaseModel, db.Model):
    """ 基础消息邮件表 """

    __tablename__ = 'test_client_event'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    mapping = db.Column(db.String(64), nullable=False)
    platform = db.Column(db.String(64), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text)
    params = db.Column(LONGTEXT)

    def __init__(self, name, mapping, platform, project_id, desc, params):
        self.name = name
        self.mapping = mapping
        self.platform = platform
        self.project_id = project_id
        self.desc = desc
        self.params = json.dumps(params, ensure_ascii=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            desc=self.desc,
            platform=self.platform,
            projectId=self.project_id,
            func=json.loads(self.params),
            mapping=self.mapping,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        Event.__table__.drop(db.session.bind)
        Event.__table__.create(db.session.bind)
