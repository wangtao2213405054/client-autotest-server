# _author: Coke
# _date: 2023/8/30 20:24

from sqlalchemy import Column, Integer, String, Text, Boolean
from application.models.base import BaseModel, db
from application import create_app

import json


class MagicMenu(BaseModel, db.Model):
    """ 魔法变量菜单表 """

    __bind_key__ = 'magicMenu'
    __tablename__ = 'test_client_magic_menu'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)  # 名称
    keyword = Column(String(64), nullable=False)  # 功能函数类映射
    sort = Column(Integer, nullable=False)  # 排序
    desc = Column(Text)  # 详细描述
    status = Column(Boolean, nullable=False)  # 状态
    node_id = Column(Integer, nullable=False)  # 节点ID
    params = Column(Text)  # 绑定的组件
    data_type = Column(String(32))  # 数据类型, menu, function

    def __init__(
            self,
            name: str,
            keyword: str,
            sort: int,
            desc: str,
            status: bool,
            node_id: int,
            data_type: str,
            params: list
    ):
        self.name = name
        self.keyword = keyword
        self.desc = desc
        self.status = status
        self.sort = sort
        self.node_id = node_id
        self.data_type = data_type
        self.params = json.dumps(params, ensure_ascii=False)

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            keyword=self.keyword,
            desc=self.desc,
            status=self.status,
            sort=self.sort,
            nodeId=self.node_id,
            type=self.data_type,
            params=json.dumps(self.params),
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(MagicMenu.__bind_key__)
        db.create_all(MagicMenu.__bind_key__)
