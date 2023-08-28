# _author: Coke
# _date: 2023/8/27 21:01

from application import socketio, utils
from flask import request


mapping_dict = {
    'mock': utils.MockFaker()
}


function_mapping = {
    'length': utils.length,
    'section': utils.section
}


@socketio.on('getMockData')
def mock_data(body: dict):
    """ 通过表达式信息, 获取需要随机的数据 """

    expression = body.get('expression')
    print(expression, '2213123')
    classify, mapping, params, function = utils.decouple(expression)
    result = getattr(mapping_dict[classify], mapping)(**params)
    print(function, '2222')

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
            result = utils.apply_string_function(result, item)

    session_id = getattr(request, 'sid', None)

    socketio.emit('reverseMockData', str(result), to=session_id)
