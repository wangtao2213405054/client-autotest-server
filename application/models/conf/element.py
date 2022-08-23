# _author: Coke
# _date: 2022/8/23 13:42

from application.models.base import BaseModel, db
from application import create_app

import json


class Element(BaseModel, db.Model):
    """ 基础消息邮件表 """

    __tablename__ = 'test_client_element'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    label = db.Column(db.String(64), nullable=False, unique=True)
    desc = db.Column(db.Text)
    platform = db.Column(db.Text, nullable=False)

    def __init__(self, name, label, desc, platform):
        self.name = name
        self.label = label
        self.desc = desc
        self.platform = json.dumps(platform, ensure_ascii=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            label=self.label,
            desc=self.desc,
            platform=json.loads(self.platform),
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        Element.__table__.drop(db.session.bind)
        Element.__table__.create(db.session.bind)
