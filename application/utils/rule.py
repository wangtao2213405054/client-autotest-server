# _author: Coke
# _date: 2022/12/7 11:38


_type = {
    'None': None,
    'Integer': int,
    'String': str,
    'Boolean': bool,
    'Array': list,
    'Object': dict,
    'Float': float
}


def rule_list_to_dict(data, key, value, types):
    """ 将列表转换为字典 """

    _dict = dict()
    for item in data:
        obj = _type.get(item[types].capitalize())
        try:
            _dict[item[key]] = obj(item[value]) if obj is not None else None
        except (TypeError, ValueError):
            return

    return _dict


if __name__ == '__main__':
    _rule = [
        {'param': 'udid', 'type': 'string', 'value': 'Test'},
        {'param': 'autoAcceptAlerts', 'type': 'Boolean', 'value': 'True'},
    ]
    print(rule_list_to_dict(_rule, 'param', 'value', 'type'))
