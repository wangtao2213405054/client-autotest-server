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


if __name__ == '__main__':
    datas = "{{ global 'name' ,min:1,max:23,change:'ws' |length|lower }}"
    print(decouple(datas))
    from faker import Faker

    fake = Faker('zh_CN')

    # 生成姓名
    name = fake.name()
    print("Name:", name)

    # 生成地址
    address = fake.address()
    print("Address:", address)

    # 生成随机文本
    text = fake.text()
    print("Text:", text)

    # 生成随机数字
    number = fake.random_int(min=1, max=100)
    print("Number:", number)

    # 生成随机日期
    date = fake.date_of_birth()
    print("Date of Birth:", date)

