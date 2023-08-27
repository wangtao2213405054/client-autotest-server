# _author: Coke
# _date: 2023/8/27 21:01

from application import socketio, utils
from flask import request
from application.ws import online_server, session_maps


mapping_dict = {
    'mock': utils.MockFaker()
}


@socketio.on('getMockData')
def mock_data(body: dict):
    """ 通过表达式信息, 获取需要随机的数据 """

    expression = body.get('expression')
    print(expression, '222')
    classify, mapping, params, function = utils.decouple(expression)
    print(classify, mapping, params, function, 333)
    result = getattr(mapping_dict[classify], mapping)(**params)
    session_id = getattr(request, 'sid', None)

    socketio.emit('reverseMockData', str(result), to=session_id)
