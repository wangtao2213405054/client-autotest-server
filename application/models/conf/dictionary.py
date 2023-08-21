# _author: Coke
# _date: 2023/8/21 14:21

from application.models.base import BaseModel, db
from application import create_app


class Dictionary(BaseModel, db.Model):
    """ 字典表 """

    __bind_key__ = 'dictionary'
    __tablename__ = 'test_client_dictionary'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)  # 元素名称
    code = db.Column(db.String(64), nullable=False, unique=True)  # 编码
    desc = db.Column(db.Text)  # 详细描述
    status = db.Column(db.Boolean, nullable=False)  # 状态

    def __init__(self, name, code, desc, status):
        self.name = name
        self.code = code
        self.desc = desc
        self.status = status

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            code=self.code,
            desc=self.desc,
            status=self.status,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


class Library(BaseModel, db.Model):
    """ 字典数据表 """

    __bind_key__ = 'library'
    __tablename__ = 'test_client_library'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)  # 名称
    code = db.Column(db.String(64), nullable=False)  # 编码
    sort = db.Column(db.Integer, nullable=False)  # 排序
    value = db.Column(db.String(64), nullable=False, unique=True)  # 数据
    value_type = db.Column(db.String(64), nullable=False)  # 数据类型
    desc = db.Column(db.Text)  # 详细描述
    status = db.Column(db.Boolean, nullable=False)  # 状态

    def __init__(self, name, code, sort, value, value_type, desc, status):
        self.name = name
        self.code = code
        self.sort = sort
        self.value = value
        self.value_type = value_type
        self.desc = desc
        self.status = status

    @property
    def result(self):
        return dict(
            id=self.id,
            name=self.name,
            code=self.code,
            desc=self.desc,
            status=self.status,
            value=self.value,
            valueType=self.value_type,
            sort=self.sort,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(Library.__bind_key__)
        db.create_all(Library.__bind_key__)
