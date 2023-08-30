# _author: Coke
# _date: 2023/8/30 23:03

from application import models, db


class Dynamic:

    def __init__(self):
        self.date()

    @staticmethod
    def date():
        _logging = models.DynamicElement(
            '请选择日期单位',
            'select',
            'String',
            '日期单位',
            'unit',
            [dict(id=1, value='s', label='秒'), dict(id=2, value='ms', label='毫秒')]
        )
        db.session.add(_logging)
        db.session.commit()
