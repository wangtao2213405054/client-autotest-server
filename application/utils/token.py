# _author: Coke
# _date: 2022/4/12 16:03

from authlib.jose import jwt
from application import utils, TOKEN_TIME_LIMIT, TOKEN_SIGN_KEY
from flask import request, g

import time
import logging
import functools


def create_token(unbridled=False, **kwargs):
    """
    生成 token
    :param unbridled: True 为 无时间限制
    :param kwargs: token 携带的用户信息
    :return:
    """

    kwargs['exp'] = (time.time() + TOKEN_TIME_LIMIT) if not unbridled else None
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
        return {'results': False, 'info': {'error': utils.TOKEN_ERR}}

    failure_time = payload.get('exp')
    if failure_time is not None and failure_time < time.time():
        return {'results': False, 'info': {'error': utils.TOKEN_EXPIRED_ERR}}

    return {'results': True, 'info': payload}


def login_required(view_func):
    """ token 校验装饰器 """
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):

        # get token
        token_jwt = request.headers.get('token')
        if not token_jwt:
            return utils.rander(utils.TOKEN_ERR)

        # analytic token
        payload = analytic_token(token_jwt)
        if not payload['results']:
            return utils.rander(payload['info']['error'])

        # get property id give global g
        user_id, username = payload['info'].get('user_id'), payload['info'].get('username')
        if not user_id:
            return utils.rander(utils.TOKEN_ERR)
        g.user_id = user_id
        g.username = username

        logging.info('user_id: {}'.format(user_id))
        return view_func(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    print(create_token(True, username='Mac', user_id=2, device='Mac14'))
