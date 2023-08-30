# _author: Coke
# _date: 2023/8/30 10:04


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


function_mapping = {
    'length': length,
    'section': section
}
