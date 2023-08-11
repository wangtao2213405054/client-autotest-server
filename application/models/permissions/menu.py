# _author: Coke
# _date: 2022/5/9 17:37

from application.models.base import BaseModel
from application import db
from sqlalchemy import Column


class Menu(BaseModel, db.Model):
    """ 权限菜单表 """

    __bind_key__ = 'menu'
    __tablename__ = 'test_client_permissions_menu'

    id = Column(db.Integer, primary_key=True)  # 主键 自增
    name = Column(db.String(32), nullable=False)  # 节点名称
    identifier = Column(db.String(512), nullable=False, unique=True)  # 标识符
    node_id = Column(db.Integer, nullable=False)  # 节点id

    def __init__(self, name=None, identifier=None, node_id=0):
        self.name = name
        self.identifier = identifier
        self.node_id = node_id

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'identifier': self.identifier,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }

