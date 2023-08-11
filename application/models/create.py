# _author: Coke
# _date: 2022/4/12 17:12

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


if __name__ == '__main__':
    from application import create_app, db
    from application.models import default
    app = create_app("local")

    with app.app_context():
        # 删除数据库所有的表
        db.drop_all()

        # 创建所有的表
        db.create_all()

        default.Project()
        default.Permissions()
