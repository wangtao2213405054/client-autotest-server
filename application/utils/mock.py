# _author: Coke
# _date: 2023/8/25 14:32

from faker import Faker
import re


def decouple(data: str):
    """
    使用正则表达式匹配出对应的数据信息
    :param data: 要匹配的正则表达式
    :return:
    """
    pattern = r"\{\{\s*([^\s|]+)\s+('[^']*')(?:\s*,\s*([^|]+))?\s*(?:\|([^%]+))*\s*(?:\|([^%]+))*\s*\}\}"

    matches = re.match(pattern, data)

    map_var = None
    function_name_var = None
    function_args = {}
    function_var = []

    if matches:
        map_var = matches.group(1)
        function_name_var = matches.group(2)[1:-1]

        # 匹配参数部分
        if matches.group(3):
            args_matches = matches.group(3).strip().split(",")
            for item in args_matches:
                key, value = item.split(":")
                function_args[key] = value.replace("'", "") if "'" in value else int(value)

        # 匹配过滤器部分
        if matches.group(4):
            function_var = matches.group(4).strip().split('|')

    return map_var, function_name_var, function_args, function_var


def apply_string_function(data: str, mapping: str) -> str:
    """
    处理正则函数, 如果存在对应的函数则进行处理, 否则返回原始数据
    :param data: 要处理的字符串
    :param mapping: 字符串的函数映射
    :return:
    """
    if hasattr(data, mapping):
        string_function = getattr(data, mapping)
        if callable(string_function):
            return string_function()

    return data


def length(data):
    """
    获取数据长度
    :param data: 要获取的数据
    :return:
    """
    return len(data)


def section(data: str, start: int = 0, end: int = 1):
    """
    数据切片
    :param data: 原始数据
    :param start: 开始切片位置
    :param end: 结束切片位置
    :return:
    """
    return data[start: end]


class MockFaker:
    """ 生成测试数据 """

    def __init__(self):
        self.fake = Faker()

    def cparagraph(self, length=50):
        self.fake = Faker('zh-CN')
        text = self.fake.text()  # 生成随机文本
        while len(text) < length:
            text += '' + self.fake.text()  # 继续生成随机文本，直到达到指定长度
        return text[:length]  # 截取指定长度的文本


mapping_dict = {
    'mock': MockFaker()
}


function_mapping = {
    'length': length,
    'section': section
}


def mock_to_string(expression):
    classify, mapping, params, function = decouple(expression)
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

        if item in function_mapping:
            result = function_mapping[item](result, **params)
        else:
            result = apply_string_function(result, item)

    return result


if __name__ == '__main__':
    datas = "{{mock 'cparagraph',length:15|section,end:2}}"
    print(decouple(datas))
