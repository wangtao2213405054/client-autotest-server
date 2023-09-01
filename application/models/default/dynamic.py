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
        min_age = models.DynamicElement(
            '请输入最小年纪',
            'input',
            'Integer',
            '最小年纪',
            'min_age'
        )
        max_age = models.DynamicElement(
            '请输入最大年纪',
            'input',
            'Integer',
            '最大年纪',
            'max_age'
        )
        _old = models.DynamicElement(
            '请输入要替换的值',
            'input',
            'String',
            '原始值',
            '_old'
        )
        _new = models.DynamicElement(
            '请输入替换后的值',
            'input',
            'String',
            '新值',
            '_new'
        )
        _extent = models.DynamicElement(
            '请输入填充长度',
            'input',
            'Integer',
            '填充长度',
            'extent'
        )
        _filler = models.DynamicElement(
            '请输入填充值',
            'input',
            'String',
            '填充值',
            'filler'
        )
        _position = models.DynamicElement(
            '请选择填充位置',
            'select',
            'String',
            '填充位置',
            'position',
            [
                dict(id=1, value='center', label='两侧'),
                dict(id=2, value='right', label='右侧'),
                dict(id=3, value='left', label='左侧')
            ]
        )

        _locale = models.DynamicElement(
            '请选择地区',
            'select',
            'String',
            '地区',
            'locale',
            [
                dict(id=1, value='zh_CN', label='中国-简体'),
                dict(id=2, value='zh_TW', label='中国-繁体'),
                dict(id=3, value='en_US', label='美国'),
                dict(id=4, value='en_GB', label='英国'),
                dict(id=5, value='ru_RU', label='俄罗斯'),
                dict(id=6, value='ja_JP', label='日本'),
                dict(id=7, value='fr_FR', label='法国'),
                dict(id=8, value='hi_IN', label='印度')

            ]
        )
        db.session.add_all(
            [
                _end, _start, _seconds, _second, _days, _hours, _weeks, _date, _formatting, _length, _minutes,
                min_age, max_age, _locale, _new, _old, _position, _extent, _filler
            ]
        )
        db.session.commit()

        _mock = models.MagicMenu('动态变量', 'mock', 3, '生成一些模拟的数据信息', True, 0, 'menu')
        db.session.add(_mock)
        db.session.commit()

        func_length = models.MagicMenu('数据长度', 'length', 3, '获取当前数据的长度', True, _mock.id, 'function')
        func_lower = models.MagicMenu('字母小写', 'lower', 3, '将所有字母变为小写', True, _mock.id, 'function')
        func_upper = models.MagicMenu('字母大写', 'upper', 3, '将所有字母变为大写', True, _mock.id, 'function')
        func_capitalize = models.MagicMenu('首字母大写', 'capitalize', 3, '将段落的首字母大写', True, _mock.id, 'function')
        func_title = models.MagicMenu('单词首字母大写', 'title', 3, '将每个单词的首字母大写', True, _mock.id, 'function')
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
        func_displace = models.MagicMenu(
            '数据替换',
            'displace',
            3,
            '将字符串中的数据替换为指定数据',
            True,
            _mock.id,
            'function',
            [_old.id, _new.id]
        )
        func_fill = models.MagicMenu(
            '数据填充',
            'fill',
            3,
            '对字符串进行填充',
            True,
            _mock.id,
            'function',
            [_position.id, _extent.id, _filler.id]
        )
        db.session.add_all([
            func_length, func_lower, func_upper, func_capitalize, func_title, func_strip, func_section, func_displace,
            func_fill
        ])
        db.session.commit()

        children_paragraph = models.MagicMenu(
            '大段文本',
            'paragraph',
            3,
            '随机生成一段文本',
            True,
            _mock.id,
            'menu',
            [_locale.id, _length.id]
        )
        children_name = models.MagicMenu(
            '姓名',
            'name',
            3,
            '生成随机一个姓名',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )
        children_first = models.MagicMenu(
            '姓氏',
            'first',
            3,
            '生成随机一个姓氏',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )
        children_last = models.MagicMenu(
            '名字',
            'last',
            3,
            '生成随机一个名字',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )
        children_phone = models.MagicMenu(
            '手机号',
            'phone',
            3,
            '生成随机一个手机号',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )
        children_company = models.MagicMenu(
            '公司',
            'company',
            3,
            '生成随机一个公司',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_address = models.MagicMenu(
            '地址',
            'address',
            3,
            '生成一个随机的地址',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_administrative = models.MagicMenu(
            '省份',
            'administrative',
            3,
            '生成一个随机的省份',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_city = models.MagicMenu(
            '城市',
            'city',
            3,
            '生成一个随机的城市',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_country = models.MagicMenu(
            '国家',
            'country',
            3,
            '生成一个随机的国家名称',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_district = models.MagicMenu(
            '地区',
            'district',
            3,
            '生成一个随机的地区',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_postcode = models.MagicMenu(
            '邮编',
            'postcode',
            3,
            '生成一个随机的邮编',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_job = models.MagicMenu(
            '职业',
            'job',
            3,
            '生成一个随机的职业',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_ssn = models.MagicMenu(
            '身份证号',
            'ssn',
            3,
            '生成一个随机的身份证号',
            True,
            _mock.id,
            'menu',
            [_locale.id, min_age.id, max_age.id]
        )
        children_license = models.MagicMenu(
            '汽车牌照',
            'license',
            3,
            '生成一个随机的车牌号',
            True,
            _mock.id,
            'menu',
            [_locale.id]
        )

        children_word = models.MagicMenu(
            '单词',
            'word',
            3,
            '生成一个随机的单词',
            True,
            _mock.id,
            'menu',
            [_locale.id]
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
            'time',
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
            children_paragraph,
            children_name,
            children_first,
            children_last,
            children_phone,
            children_company,
            children_address,
            children_administrative,
            children_city,
            children_country,
            children_district,
            children_postcode,
            children_job,
            children_ssn,
            children_license,
            children_word,
            children_email,
            children_datetime,
            children_date,
            children_time,
            children_timestamp,
            children_week,
            children_now,
        ])
        db.session.commit()
