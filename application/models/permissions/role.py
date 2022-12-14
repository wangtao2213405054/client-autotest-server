# _author: Coke
# _date: 2022/5/11 15:07

from application.models.base import BaseModel
from application import db
from sqlalchemy import Column

import json


class Role(BaseModel, db.Model):
    """ 角色表 """

    __bind_key__ = 'role'
    __tablename__ = 'test_client_permissions_role'

    id = Column(db.Integer, primary_key=True)  # 主键 自增
    name = Column(db.String(32), nullable=False)  # 角色名称
    identifier = Column(db.String(512), nullable=False, unique=True)  # 标识符
    permissions_api = Column(db.Text)  # 接口权限列表
    permissions_menu = Column(db.Text)  # 菜单权限列表

    def __init__(self, name=None, identifier=None, permissions_api: list = None, permissions_menu: list = None):
        self.name = name
        self.identifier = identifier
        self.permissions_api = json.dumps(permissions_api)
        self.permissions_menu = json.dumps(permissions_menu)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'identifier': self.identifier,
            'permissionsApi': json.loads(self.permissions_api) if self.permissions_api else [],
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
