# _author: Coke
# _date: 2022/12/29 16:23

from application.models.base import BaseModel, db
from application import create_app
from sqlalchemy.dialects.mysql import LONGTEXT


class Api(BaseModel, db.Model):
    """ 接口表 """

    __bind_key__ = 'api'
    __tablename__ = 'test_client_api'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # 主键
    project_id = db.Column(db.Integer, nullable=False)  # 项目ID
    name = db.Column(db.String(32), nullable=False)  # 接口名称
    path = db.Column(db.Text, nullable=False)  # 接口路径
    body = db.Column(LONGTEXT, nullable=False)  # 接口 response 结构体

    def __init__(self, project_id, name, path, body):
        self.project_id = project_id
        self.name = name
        self.path = path
        self.body = body

    @property
    def result(self):
        return dict(
            id=self.id,
            project_id=self.project_id,
            name=self.name,
            path=self.path,
            body=self.body,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(Api.__bind_key__)
        db.create_all(Api.__bind_key__)
