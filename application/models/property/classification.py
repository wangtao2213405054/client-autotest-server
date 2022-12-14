# _author: Coke
# _date: 2022/4/30 01:36

from application.models.base import BaseModel
from application import db
from sqlalchemy import Column


class Classification(BaseModel, db.Model):
    """ 公司关系表 """

    __bind_key__ = 'classification'
    __tablename__ = 'test_client_classification'

    id = Column(db.Integer, primary_key=True)  # 主键 自增
    name = Column(db.String(32), nullable=False)  # 节点名称
    node_id = Column(db.Integer, nullable=False)  # 节点id

    def __init__(self, name=None, node_id=0):
        self.name = name
        self.node_id = node_id

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
