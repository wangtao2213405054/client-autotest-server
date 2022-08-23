# _author: Coke
# _date: 2022/8/23 17:23

from application import models, db


class User:

    def __init__(self):

        self.classification = models.Classification('客户端')
        db.session.add(self.classification)
        db.session.commit()

        self.department = models.Classification('效能部', self.classification.id)
        db.session.add(self.department)
        db.session.commit()

        self.role = models.Role('超级管理员', 'admin')
        db.session.add(self.role)
        db.session.commit()

        self.user = models.User(
            'admin',
            'admin@client.com',
            '7c4a8d09ca3762af61e59520943dc26494f8941b',
            '12345678910',
            role=self.role.id,
            avatar_url='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            node=self.department.id,
            department=[self.classification.id, self.department.id]
        )
        db.session.add(self.user)
        db.session.commit()
