# _author: Coke
# _date: 2022/8/16 15:53

from application.models.base import BaseModel, db
from application import create_app

import json


class MessageDingTalk(BaseModel, db.Model):
    """ 消息配置钉钉机器人数据表 """

    __tablename__ = 'test_client_message_talk'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    tokens = db.Column(db.Text, nullable=False)
    at_all = db.Column(db.String(32), nullable=False)
    at_mobile = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __init__(self, project_id, tokens, at_all, at_mobile, status):
        self.project_id = project_id
        self.tokens = json.dumps(tokens, ensure_ascii=False)
        self.at_all = at_all
        self.at_mobile = json.dumps(at_mobile, ensure_ascii=False)
        self.status = status

    def to_dict(self):
        return dict(
            id=self.id,
            projectId=self.project_id,
            tokens=json.loads(self.tokens),
            atAll=self.at_all,
            atMobile=json.loads(self.at_mobile),
            status=self.status,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        MessageDingTalk.__table__.drop(db.session.bind)
        MessageDingTalk.__table__.create(db.session.bind)