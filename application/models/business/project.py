# _author: Coke
# _date: 2022/5/3 12:53

from application.models.base import BaseModel, db
from application import create_app
from sqlalchemy import Column


class Project(BaseModel, db.Model):
    """ 项目表 """

    __tablename__ = 'test_interface_project'

    id = Column(db.Integer, primary_key=True)  # 主键
    name = Column(db.String(32), nullable=False, unique=True)  # 项目名称
    describe = Column(db.String(512))  # 项目描述
    avatar = Column(db.String(512))  # 头像
    create_user = Column(db.String(256), nullable=False)  # 创建人
    create_id = Column(db.Integer)  # 创建人ID

    def __init__(self, name=None, describe=None, avatar=None, create_user=None, create_id=None):
        self.name = name
        self.describe = describe
        self.avatar = avatar
        self.create_user = create_user
        self.create_id = create_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'avatar': self.avatar,
            'createUser': self.create_user,
            'createId': self.create_id,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        Project.__table__.drop(db.session.bind)  # 删除表
        Project.__table__.create(db.session.bind)  # 创建表
