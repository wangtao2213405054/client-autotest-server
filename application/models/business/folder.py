# _author: Coke
# _date: 2022/5/27 20:51

from application.models.base import BaseModel
from sqlalchemy import Column, String, Integer
from application import create_app, db


class Folder(BaseModel, db.Model):
    """ api模块列表 """

    __bind_key__ = 'folder'
    __tablename__ = 'test_client_folder'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)  # 主键
    project_id = Column(Integer, nullable=False)  # 所属项目
    name = Column(String(32), nullable=False)  # 模块名称
    node_id = Column(Integer)  # 节点ID
    data_type = Column(String(32))  # 文件类型
    sort = Column(Integer)  # 排序

    def __init__(self, project_id=None, name=None, data_type='folder', node_id=0, sort=1):
        self.project_id = project_id,
        self.name = name,
        self.data_type = data_type
        self.node_id = node_id
        self.sort = sort

    @property
    def result(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.data_type,
            'projectId': self.project_id,
            'nodeId': self.node_id,
            'createTime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'updateTime': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        db.drop_all(Folder.__bind_key__)
        db.create_all(Folder.__bind_key__)
