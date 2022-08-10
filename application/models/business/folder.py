# _author: Coke
# _date: 2022/5/27 20:51

from application.models.base import BaseModel
from sqlalchemy import Column
from application import create_app, db


class Folder(BaseModel, db.Model):
    """ api模块列表 """

    __tablename__ = 'test_interface_folder'

    id = Column(db.Integer, primary_key=True)  # 主键
    project_id = Column(db.Integer, nullable=False)  # 所属项目
    name = Column(db.String(32), nullable=False)  # 模块名称
    node_id = Column(db.Integer)  # 节点属性
    identifier = Column(db.String(32), nullable=False)  # 模块标识符 folder or api

    def __init__(self, project_id=None, name=None, node_id=0, identifier='folder'):
        self.project_id = project_id,
        self.name = name,
        self.node_id = node_id,
        self.identifier = identifier

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'projectId': self.project_id,
            'identifier': self.identifier,
            'nodeId': self.node_id,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        Folder.__table__.drop(db.session.bind)
        Folder.__table__.create(db.session.bind)
