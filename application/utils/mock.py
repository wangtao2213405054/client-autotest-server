# _author: Coke
# _date: 2023/8/25 14:32

from faker import Faker
import re


def decouple(data: str):
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


class MockFaker:
    """ 生成测试数据 """

    def __init__(self):
        self.fake = Faker()

    def cparagraph(self, length=15):
        self.fake = Faker('zh_CN')
        text = self.fake.text()  # 生成随机文本
        while len(text) < length:
            text += '' + self.fake.text()  # 继续生成随机文本，直到达到指定长度
        return text[:length]  # 截取指定长度的文本


if __name__ == '__main__':
    datas = "{{ mock 'cparagraph' }}"
    print(decouple(datas))
