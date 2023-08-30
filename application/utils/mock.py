# _author: Coke
# _date: 2023/8/25 14:32

from application import utils
from faker import Faker

import functools
import datetime
import time
import re


def set_locale(locale):
    """ 切换 Faker 语言的装饰器 """
    def decorator(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            old_locale = self.fake.locale
            new_faker = Faker(locale)
            self.fake = new_faker  # 切换语言类型
            result = method(self, *args, **kwargs)
            self.fake = Faker(old_locale)  # 恢复原始语言类型
            return result

        return wrapper

    return decorator


class MockFaker:
    """ 生成测试数据 """

    def __init__(self):
        self.fake = Faker()

    @set_locale('zh_CN')
    def cparagraph(self, length=50):
        """ 模拟一段文本 """
        text = self.fake.text()  # 生成随机文本
        while len(text) < length:
            text += '' + self.fake.text()  # 继续生成随机文本，直到达到指定长度
        return text[:length]  # 截取指定长度的文本

    @set_locale('zh_CN')
    def cname(self):
        """ 模拟一个名字 """
        return self.fake.name()

    @set_locale('zh_CN')
    def cfirst(self):
        """ 模拟一个姓氏 """
        return self.fake.last_name()

    @set_locale('zh_CN')
    def clast(self):
        """ 模拟一个名字 """
        return self.fake.first_name()

    @set_locale('zh_CN')
    def cphone(self):
        """ 模拟一个手机号 """
        return self.fake.phone_number()

    def email(self):
        """ 模拟一个邮件 """
        return self.fake.email()

    @set_locale('zh_CN')
    def ccompany(self):
        """ 模拟一个公司 """
        return self.fake.company()

    @set_locale('zh_CN')
    def caddress(self):
        """ 模拟一个地址 """
        return self.fake.address()

    def datetime(self, formatting='%Y-%m-%d %H:%M:%S'):
        """ 模拟一个日期时间 """
        return self.fake.date_time_this_decade().strftime(formatting)

    def date(self, formatting='%Y-%m-%d'):
        """ 模拟一个日期 """
        return self.fake.date_this_decade().strftime(formatting)

    def time(self, formatting='%H:%M:%S'):
        """ 模拟一个时间 """
        random_time = self.fake.time()
        return time.strftime(formatting, time.strptime(random_time, '%H:%M:%S'))

    @staticmethod
    def timestamp(unit='s'):
        """ 获取当前时间戳 """
        return int(time.time()) if unit == 's' else int(time.time() * 1000)

    @staticmethod
    def week(unit='year'):
        """ 获取当前周(月份或年份) """
        current_date = datetime.datetime.now()
        if unit == 'year':
            # 获取当前年份的周数
            return current_date.isocalendar()[1]
        elif unit == 'month':
            start_of_month = datetime.datetime(current_date.year, current_date.month, 1)
            # 计算当前日期在当月的周数
            return (current_date - start_of_month).days // 7 + 1
        else:
            return 0

    @staticmethod
    def now(formatting='%Y-%m-%d %H:%M:%S', days=0, seconds=0, minutes=0, hours=0, weeks=0):
        """ 获取当前时间并可以添加偏移 """
        current_date = datetime.datetime.now()
        current_date += datetime.timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours, weeks=weeks)

        return current_date.strftime(formatting)


mapping_dict = {
    'mock': MockFaker()
}


def decouple(expression: str):
    """
    使用正则表达式匹配出对应的数据信息
    :param expression: 要匹配的正则表达式
    :return:
    """
    pattern = r"\{\{\s*([^\s|]+)\s+('[^']*')(?:\s*,\s*([^|]+))?\s*(?:\|([^%]+))*\s*(?:\|([^%]+))*\s*\}\}"

    matches = re.match(pattern, expression)

    classify = None
    mapping = None
    params = {}
    function = []

    if matches:
        classify = matches.group(1)
        mapping = matches.group(2)[1:-1]

        # 匹配参数部分
        if matches.group(3):
            args_matches = matches.group(3).strip().split(",")
            for item in args_matches:
                key, value = item.split(":")
                params[key] = value.replace("'", "") if "'" in value else int(value)

        # 匹配过滤器部分
        if matches.group(4):
            function = matches.group(4).strip().split('|')

    result = getattr(mapping_dict[classify], mapping)(**params)

    for item in function:
        params = dict()
        if ',' in item:
            function_params = item.split(',')
            item = function_params[0]
            _params = function_params[1:]

            for param in _params:
                key, value = param.split(":")
                params[key] = value.replace("'", "") if "'" in value else int(value)

        if item in utils.function_mapping:
            result = utils.function_mapping[item](result, **params)
        else:
            result = utils.apply_string_function(result, item)

    return result


if __name__ == '__main__':
    datas = "{{mock 'cparagraph',length:15|section,end:2}}"
    print(decouple(datas))
