# _author: Coke
# _date: 2022/12/29 13:59

from application.models.base import BaseModel, db
from application import create_app


class Domain(BaseModel, db.Model):
    """ 域名表 """

    __bind_key__ = 'domain'
    __tablename__ = 'test_client_domain'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # 主键
    project_id = db.Column(db.Integer, nullable=False)  # 项目ID
    name = db.Column(db.String(32), nullable=False)  # 域名名称
    domain = db.Column(db.String(512), nullable=False)  # 域名信息
    protocol = db.Column(db.String(32), nullable=False)  # 协议
    port = db.Column(db.String(32), nullable=False)  # 端口

    def __init__(self, project_id, name, domain, protocol, port):
        self.project_id = project_id
        self.name = name
        self.domain = domain
        self.protocol = protocol
        self.port = port

    @property
    def result(self):
        return dict(
            id=self.id,
            projectId=self.project_id,
            name=self.name,
            domain=self.domain,
            protocol=self.protocol,
            port=self.port,
            createTime=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            updateTime=self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


if __name__ == '__main__':
    app = create_app('local')
    with app.app_context():
        db.drop_all(Domain.__bind_key__)
        db.create_all(Domain.__bind_key__)
