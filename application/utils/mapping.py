# _author: Coke
# _date: 2023/8/30 10:04


def apply_string_function(data: str, mapping: str, **kwargs) -> str:
    """
    处理正则函数, 如果存在对应的函数则进行处理, 否则返回原始数据
    :param data: 要处理的字符串
    :param mapping: 字符串的函数映射
    :return:
    """
    if hasattr(data, mapping):
        string_function = getattr(data, mapping)
        if callable(string_function):
            return string_function(**kwargs)

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


def displace(data: str, _old='', _new=''):
    """
    数据替换
    :param data: 原始数据
    :param _old: 要替换的值
    :param _new: 替换后的值
    :return:
    """
    return data.replace(_old, _new)


def fill(data: str, extent: int = 1, filler: str = '*', position: str = 'center'):
    """
    数据填充
    :param data: 原始数据
    :param extent: 填充长度
    :param filler: 填充值
    :param position: 填充位置
    :return:
    """

    if position == 'center':
        return data.center(len(data) + extent * 2, filler)

    elif position == 'right':
        return data.ljust(len(data) + extent, filler)

    else:
        return data.rjust(len(data) + extent, filler)


function_mapping = {
    'length': length,
    'section': section,
    'displace': displace,
    'fill': fill
}
