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
            pass

    return _dict


def resolve(steps):
    """ 将测试用例解析成驱动端可执行的结构 """

    _resolve = []
    for case in steps:
        _resolve_case = dict(
            id=case.get('id'),
            mapping=case.get('mapping'),
            name=case.get('name'),
            subset=case.get('subset'),
            desc=case.get('desc'),
            params=rule_list_to_dict(case.get('func'), 'param', 'default', 'dataType'),
            screenshot=case.get('screenshot')
        )
        _resolve.append(_resolve_case)

    return _resolve


if __name__ == '__main__':
    _rule = [
        {'param': 'did', 'type': 'Integer', 'value': 'Test'},
        {'param': 'autoAcceptAlerts', 'type': 'Boolean', 'value': 'True'},
    ]
    print(rule_list_to_dict(_rule, 'param', 'value', 'type'))
