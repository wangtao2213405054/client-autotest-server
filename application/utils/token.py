# _author: Coke
# _date: 2022/4/12 16:03

from authlib.jose import jwt
from application import TOKEN_SIGN_KEY, TOKEN_TIME_LIMIT
from application.utils.response import rander
from flask import request, g

import time
import logging
import functools


def create_token(**kwargs):
    """ 生成 token """

    kwargs['exp'] = time.time() + TOKEN_TIME_LIMIT
    header = {
        'alg': 'HS256'
    }
    token = jwt.encode(header, kwargs, TOKEN_SIGN_KEY)

    return token.decode()


def analytic_token(token):
    """ 解析token """

    try:
        payload = jwt.decode(token, TOKEN_SIGN_KEY)
    except Exception as e:
        logging.error(f'analytic token fail error log: {e}')
        return {'results': False, 'info': {'error': 'TOKEN_ERR'}}

    failure_time = payload.get('exp')
    if not failure_time or failure_time < time.time():
        return {'results': False, 'info': {'error': 'TOKEN_EXPIRED_ERR'}}

    return {'results': True, 'info': payload}


def login_required(view_func):
    """ token 校验装饰器 """
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):

        # get token
        token_jwt = request.headers.get('token')
        if not token_jwt:
            return rander('TOKEN_ERR')

        # analytic token
        payload = analytic_token(token_jwt)
        if not payload['results']:
            return rander(payload['info']['error'])

        # get property id give global g
        user_id, user_name = payload['info'].get('user_id'), payload['info'].get('user_name')
        if not user_id:
            return rander('TOKEN_ERR')
        g.user_id = user_id
        g.user_name = user_name

        logging.info('user_id: {}'.format(user_id))
        return view_func(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    print(create_token())
