# _author: Coke
# _date: 2022/4/12 14:37

import time
import json
import logging

CODE = {
    'OK': {'code': 1, 'message': '服务接口调用成功'},
    'TOKEN_ERR': {'code': 4001, 'message': '非法用户令牌'},
    'TOKEN_EXPIRED_ERR': {'code': 4002, 'message': '用户令牌过期'},
    'DATABASE_ERR': {'code': 4104, 'message': '数据库操作错误'},
    'BODY_ERR': {'code': 4102, 'message': 'Body不可为空'},
    'DATA_ERR': {'code': 4103, 'message': '请求参数错误'},
    'USER_ERR': {'code': 4105, 'message': '账号密码错误'},
    'MOBILE_ERR': {'code': 4106, 'message': '手机号错误'},
    'PASSWORD_ERR': {'code': 4107, 'message': '两次密码不匹配'},
    'ROLE_ERR': {'code': 4100, 'message': '暂无权限, 请联系管理员'},
    'SOCKET_ERR': {'code': 4201, 'message': '设备通讯失败，请稍后再试'},
    'SOCKET_TIMEOUT': {'code': 4202, 'message': '设备通讯超时'}
}


def rander(code, msg=None, data=None):
    """ 返回json 信息 """
    if isinstance(code, str):
        code = code.upper()
    back = {
        'code': CODE.get(code).get('code') if isinstance(code, str) else code,
        'ts': int(time.time()),
        'msg': msg if msg else (CODE.get(code).get('message') if CODE.get(code) else None),
        'data': data if data else []
    }
    logging.debug(back)
    return json.dumps(back, ensure_ascii=False)


def paginate_structure(data, total, page, page_size):
    """ 返回一个分页通用的数据结构 """
    return {
        'items': data,
        'total': total,
        'totalPage': total // page_size + 1 if total % page_size else total // page_size,
        'page': page,
        'pageSize': page_size,
    }


if __name__ == '__main__':
    print(rander('token_err'))
