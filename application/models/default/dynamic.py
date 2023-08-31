# _author: Coke
# _date: 2023/8/30 23:03

from application import models, db


class Dynamic:

    def __init__(self):
        self.default()

    @staticmethod
    def default():
        _second = models.DynamicElement(
            '请选择日期单位',
            'select',
            'String',
            '秒级单位',
            'unit',
            [dict(id=1, value='s', label='秒'), dict(id=2, value='ms', label='毫秒')]
        )
        _length = models.DynamicElement(
            '请输入文本长度',
            'input',
            'Integer',
            '文本长度',
            'length'
        )
        _formatting = models.DynamicElement(
            '%Y-%m-%d %H:%M:%S',
            'input',
            'String',
            '时间格式',
            'formatting'
        )
        _date = models.DynamicElement(
            '请选择日期单位',
            'select',
            'String',
            '日期单位',
            'unit',
            [dict(id=1, value='year', label='年'), dict(id=2, value='month', label='月')]
        )
        _days = models.DynamicElement(
            '正整数或负整数',
            'input',
            'Integer',
            '偏移天',
            'days'
        )
        _weeks = models.DynamicElement(
            '正整数或负整数',
            'input',
            'Integer',
            '偏移周',
            'weeks'
        )
        _hours = models.DynamicElement(
            '正整数或负整数',
            'input',
            'Integer',
            '偏移小时',
            'hours'
        )
        _minutes = models.DynamicElement(
            '正整数或负整数',
            'input',
            'Integer',
            '偏移分钟',
            'minutes'
        )
        _seconds = models.DynamicElement(
            '正整数或负整数',
            'input',
            'Integer',
            '偏移秒',
            'seconds'
        )
        _start = models.DynamicElement(
            '请输入起始位',
            'input',
            'Integer',
            '起始位',
            'start'
        )
        _end = models.DynamicElement(
            '请输入结束位',
            'input',
            'Integer',
            '结束位',
            'end'
        )
        db.session.add_all(
            [_end, _start, _seconds, _second, _days, _hours, _weeks, _date, _formatting, _length, _minutes]
        )
        db.session.commit()

        _mock = models.MagicMenu('动态变量', 'mock', 3, '生成一些模拟的数据信息', True, 0, 'menu')
        db.session.add(_mock)
        db.session.commit()

        func_length = models.MagicMenu('数据长度', 'length', 3, '获取当前数据的长度', True, _mock.id, 'function')
        func_lower = models.MagicMenu('字母小写', 'lower', 3, '将所有字母变为小写', True, _mock.id, 'function')
        func_upper = models.MagicMenu('字母大写', 'upper', 3, '将所有字母变为大写', True, _mock.id, 'function')
        func_capitalize = models.MagicMenu('首字母大写', 'capitalize', 3, '将段落的首字母大写', True, _mock.id, 'function')
        func_title = models.MagicMenu('单词首字母大写', 'title', 3, '将每个单次的首字母大写', True, _mock.id, 'function')
        func_strip = models.MagicMenu('去除空白字符', 'strip', 3, '去掉字符串前后空白字符', True, _mock.id, 'function')
        func_section = models.MagicMenu(
            '数据切片',
            'section',
            3,
            '取出序列中一个范围对应的元素',
            True,
            _mock.id,
            'function',
            [_start.id, _end.id]
        )
        db.session.add_all([func_length, func_lower, func_upper, func_capitalize, func_title, func_strip, func_section])
        db.session.commit()

        children_zh_paragraph = models.MagicMenu(
            '中文大段文本',
            'cparagraph',
            3,
            '生成随机一段的中文段落',
            True,
            _mock.id,
            'menu',
            [_length.id]
        )
        children_zh_name = models.MagicMenu(
            '中文姓名',
            'cname',
            3,
            '生成随机一个中文姓名',
            True,
            _mock.id,
            'menu'
        )
        children_zh_first = models.MagicMenu(
            '中文姓',
            'cfirst',
            3,
            '生成随机一个中文姓氏',
            True,
            _mock.id,
            'menu'
        )
        children_zh_last = models.MagicMenu(
            '中文名',
            'clast',
            3,
            '生成随机一个中文名字',
            True,
            _mock.id,
            'menu'
        )
        children_zh_phone = models.MagicMenu(
            '国内手机号',
            'cphone',
            3,
            '生成随机一个国内手机号',
            True,
            _mock.id,
            'menu'
        )
        children_zh_company = models.MagicMenu(
            '中文公司',
            'ccompany',
            3,
            '生成随机一个中文公司',
            True,
            _mock.id,
            'menu'
        )

        children_zh_address = models.MagicMenu(
            '中文地址',
            'caddress',
            3,
            '生成随机一个中文地址',
            True,
            _mock.id,
            'menu'
        )

        children_email = models.MagicMenu(
            '邮件',
            'email',
            3,
            '生成随机一个邮件',
            True,
            _mock.id,
            'menu'
        )

        children_datetime = models.MagicMenu(
            '日期时间',
            'datetime',
            3,
            '生成一段随机的日期时间, 默认格式为: %Y-%m-%d %H:%M:%S',
            True,
            _mock.id,
            'menu',
            [_formatting.id]
        )

        children_date = models.MagicMenu(
            '日期',
            'date',
            3,
            '生成一段随机的日期, 默认格式为: %Y-%m-%d',
            True,
            _mock.id,
            'menu',
            [_formatting.id]
        )

        children_time = models.MagicMenu(
            '时间',
            'date',
            3,
            '生成一段随机的时间, 默认格式为: %H:%M:%S',
            True,
            _mock.id,
            'menu',
            [_formatting.id]
        )

        children_timestamp = models.MagicMenu(
            '时间戳',
            'timestamp',
            3,
            '获取当前的时间戳',
            True,
            _mock.id,
            'menu',
            [_second.id]
        )

        children_week = models.MagicMenu(
            '当前周',
            'week',
            3,
            '获取当前日期是第几周, 可选当前年和当前月',
            True,
            _mock.id,
            'menu',
            [_date.id]
        )

        children_now = models.MagicMenu(
            '当前日期时间',
            'now',
            3,
            '获取当前日期时间',
            True,
            _mock.id,
            'menu',
            [_formatting.id, _days.id, _weeks.id, _hours.id, _minutes.id, _seconds.id]
        )

        db.session.add_all([
            children_zh_paragraph,
            children_zh_name,
            children_zh_first,
            children_zh_last,
            children_zh_phone,
            children_zh_company,
            children_zh_address,
            children_email,
            children_datetime,
            children_date,
            children_time,
            children_timestamp,
            children_week,
            children_now
        ])
        db.session.commit()
