# _author: Coke
# _date: 2023/8/30 21:32

from sqlalchemy import Column, Integer, String, Text
from application.models.base import BaseModel, db
from application import create_app

import json


class DynamicElement(BaseModel, db.Model):
    """ 动态组件表 """

    __bind_key__ = 'dynamicElement'
    __tablename__ = 'test_client_dynamic_element'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    placeholder = Column(String(64))  # 站位文本提示
    element = Column(String(32), nullable=False)  # 组件类型 input select
    data_type = Column(String(32))  # 数据类型 Integer String
    name = Column(String(32), nullable=False)  # 名称
    expression = Column(String(64), nullable=False)  # 要绑定的表达式信息
    options = Column(Text)  # 组件额外绑定的参数 List

    def __init__(self, placeholder: str, element: str, data_type: str, name: str, expression: str, options: list):
        self.placeholder = placeholder
        self.element = element
        self.data_type = data_type
        self.name = name
        self.expression = expression
        self.options = json.dumps(options, ensure_ascii=False)

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            placeholder=self.placeholder,
            element=self.element,
            type=self.data_type,
            expression=self.expression,
            options=json.loads(self.options),
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(DynamicElement.__bind_key__)
        db.create_all(DynamicElement.__bind_key__)
