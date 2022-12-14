# _author: Coke
# _date: 2022/4/12 17:09

from application.models.base import BaseModel
from application import create_app, db
from sqlalchemy import Column

import json


class User(BaseModel, db.Model):
    """ 用户表 """

    __bind_key__ = 'user'
    __tablename__ = 'test_client_user'

    id = Column(db.Integer, primary_key=True)  # 主键 自增
    name = Column(db.String(32), nullable=False)  # 名称
    email = Column(db.String(64), unique=True, nullable=False)  # 邮箱 不可重复
    password = Column(db.String(512), nullable=False)  # 密码
    mobile = Column(db.String(11), unique=True, nullable=False)  # 手机号 不可重复
    avatar_url = Column(db.String(512))  # 头像
    state = Column(db.Boolean, nullable=False)  # 用户在职状态
    node = Column(db.Integer)  # 节点
    role = Column(db.Integer, nullable=False)  # 角色
    department = Column(db.String(64))  # 部门

    def __init__(
            self,
            name=None,
            email=None,
            password=None,
            mobile=None,
            avatar_url=None,
            state=True,
            node=None,
            department=None,
            role=None
    ):
        self.name = name
        self.email = email
        self.password = password
        self.mobile = mobile
        self.avatar_url = avatar_url
        self.state = state
        self.node = node
        self.role = role
        self.department = json.dumps(department,ensure_ascii=False)

    @property
    def to_dict(self):
        """ 将对象转换为字典数据 """
        user_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'avatarUrl': self.avatar_url,
            'state': self.state,
            'department': json.loads(self.department) if self.department else [],
            'role': self.role,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict


if __name__ == '__main__':
    app = create_app('local')
    # 删除并创建表
    with app.app_context():
        db.drop_all()  # delete
        db.create_all()  # create
