# _author: Coke
# _date: 2022/8/15 14:01

from application.models.base import BaseModel, db
from application import create_app

import json


class MessageEmail(BaseModel, db.Model):
    """ 基础消息邮件表 """

    __bind_key__ = 'email'
    __tablename__ = 'test_client_message_email'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)  # 项目ID
    host = db.Column(db.String(64), nullable=False)  # 主机地址
    title = db.Column(db.String(24), nullable=False)  # 标题
    sender = db.Column(db.String(128), nullable=False)  # 发送人
    password = db.Column(db.String(128), nullable=False)  # 密码
    receivers = db.Column(db.Text, nullable=False)  # 接收人
    state = db.Column(db.Boolean, nullable=False)  # 状态

    def __init__(self, project_id, host, title, sender, password, receivers, state):
        self.project_id = project_id
        self.host = host
        self.title = title
        self.sender = sender
        self.password = password
        self.receivers = json.dumps(receivers, ensure_ascii=False)
        self.state = state

    @property
    def to_dict(self):
        return dict(
            id=self.id,
            projectId=self.project_id,
            host=self.host,
            title=self.title,
            sender=self.sender,
            password=self.password,
            receivers=json.loads(self.receivers),
            state=self.state,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(MessageEmail.__bind_key__)
        db.create_all(MessageEmail.__bind_key__)
