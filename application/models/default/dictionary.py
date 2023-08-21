# _author: Coke
# _date: 2023/8/21 22:55

from application import models, db


class Dictionary:

    def __init__(self):
        self.logging()
        self.operation()
        self.data_type()
        self.boolean()

    @staticmethod
    def logging():
        _logging = models.Dictionary('日志', 'logging', '日志等级')
        db.session.add(_logging)
        db.session.commit()
        _type = 'String'
        debug = models.Library('DEBUG', _logging.code, 1, 'DEBUG', _type, 'DEBUG 日志等级')
        info = models.Library('INFO', _logging.code, 2, 'INFO', _type, 'INFO 日志等级')
        error = models.Library('ERROR', _logging.code, 3, 'ERROR', _type, 'ERROR 日志等级')
        warning = models.Library('WARNING', _logging.code, 4, 'WARNING', _type, 'WARNING 日志等级')
        critical = models.Library('CRITICAL', _logging.code, 5, 'CRITICAL', _type, 'CRITICAL 日志等级')

        db.session.add_all([debug, info, error, warning, critical])
        db.session.commit()

    @staticmethod
    def operation():
        _operation = models.Dictionary('运算', 'operation', '运算公式(比较运算和成员运算)')
        db.session.add(_operation)
        db.session.commit()
        _type = 'String'
        equality = models.Library('等于', _operation.code, 1, '=', _type, '比较对象是否相等')
        unlikeness = models.Library('不等于', _operation.code, 2, '!=', _type, '比较两个对象是否不相等')
        greater = models.Library('大于', _operation.code, 3, '>', _type, '返回x是否大于y')
        greater_equality = models.Library('大于等于', _operation.code, 4, '>=', _type, '返回x是否大于等于y')
        less = models.Library('小于', _operation.code, 5, '<', _type, '返回x是否小于y')
        less_equality = models.Library('小于等于', _operation.code, 6, '<=', _type, '返回x是否小于等于y')
        _in = models.Library(
            '在...里面',
            _operation.code,
            7,
            'in',
            _type,
            '如果在指定的序列中找到值返回 True，否则返回 False'
        )
        out = models.Library(
            '不在...里面',
            _operation.code,
            8,
            'out',
            _type, '如果在指定的序列中没有找到值返回 True，否则返回 False'
        )

        db.session.add_all([equality, unlikeness, greater, greater_equality, less_equality, less, _in, out])
        db.session.commit()

    @staticmethod
    def data_type():
        _operation = models.Dictionary('类型', 'type', '数据类型')
        db.session.add(_operation)
        db.session.commit()
        _type = 'String'
        none = models.Library('空值', _operation.code, 1, 'None', _type, '表示空、缺失或者没有值的情况')
        integer = models.Library(
            '整数',
            _operation.code,
            2,
            'Integer',
            _type,
            '整数是不带小数部分的数值。整数类型通常用来表示整数值，即正整数、负整数和零'
        )
        string = models.Library(
            '字符串',
            _operation.code,
            3,
            'String',
            _type,
            '表示文本的数据类型, 可以包含字母、数字、符号以及空格等字符'
        )
        boolean = models.Library('布尔值', _operation.code, 4, 'Boolean', _type, '表示逻辑上的真和假')
        _float = models.Library(
            '浮点数/小数',
            _operation.code,
            5,
            'Float',
            _type,
            '表示带有小数部分的数值, 浮点数可以用来表示实数，包括小数、分数和指数等'
        )
        array = models.Library(
            '数组/列表',
            _operation.code,
            6,
            'Array',
            _type,
            '列表允许你在一个变量中存储多个值，这些值可以是相同类型或不同类型的数据'
        )
        _object = models.Library(
            '对象/字典',
            _operation.code,
            7,
            'Object',
            _type,
            '字典允许你使用一个键来访问与之关联的值，类似于现实生活中的字典，你可以通过单词（键）找到对应的定义（值）'
        )
        db.session.add_all([none, integer, string, boolean, _float, array, _object])
        db.session.commit()

    @staticmethod
    def boolean():
        _boolean = models.Dictionary('布尔', 'boolean', '表示逻辑上的真和假')
        db.session.add(_boolean)
        db.session.commit()
        _type = 'Boolean'
        true = models.Library('True', _boolean.code, 1, 'True', _type, '逻辑真')
        false = models.Library('False', _boolean.code, 2, 'False', _type, '逻辑假')
        db.session.add_all([true, false])
        db.session.commit()
