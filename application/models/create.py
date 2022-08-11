# _author: Coke
# _date: 2022/4/12 17:12

from application import create_app, db
from application.models.business.project import Project
from application.models.property.user import User
from application.models.property.classification import Classification
from application.models.permissions.role import Role


if __name__ == '__main__':
    app = create_app("local")
    with app.app_context():
        # 删除数据库所有的表
        db.drop_all()

        # 创建所有的表
        db.create_all()

        classification = Classification('陨星科技')
        db.session.add(classification)
        db.session.commit()
        classification1 = Classification('测试部', classification.id)

        db.session.add(classification)
        db.session.add(classification1)
        db.session.commit()

        role = Role('超级管理员', 'admin')
        db.session.add(role)
        db.session.commit()
        user = User('Coke', 'coke@qq.com', '7c4a8d09ca3762af61e59520943dc26494f8941b', '13520421043',
                    role=role.id)
        db.session.add(user)
        db.session.commit()
