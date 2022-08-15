# _author: Coke
# _date: 2022/8/15 13:58

from application.api import api
from application import utils, db, models
from flask import request

import logging
import json


@api.route('/message/email/info', methods=['GET', 'POST'])
def get_message_email_info():
    """
    获取 email 配置信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    project_id = body.get('projectId')

    if not project_id:
        return utils.rander('DATA_ERR')

    email = models.MessageEmail.query.filter_by(project_id=project_id).first()

    if not email:
        default = dict(
            projectId=project_id,
            host=None,
            title=None,
            sender=None,
            password=None,
            receivers=[],
            state=False
        )
        return utils.rander('OK', data=default)

    return utils.rander('OK', data=email.to_dict())


@api.route('/message/email/edit', methods=['POST', 'PUT'])
def edit_message_email_info():
    """
    新增/修改 email 信息
    :return:
    """
    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    email_id = body.get('id')
    project_id = body.get('projectId')
    host = body.get('host')
    title = body.get('title')
    sender = body.get('sender')
    password = body.get('password')
    receivers = body.get('receivers')
    state = body.get('state')

    if not all([host, title, sender, password, receivers]):
        return utils.rander('DATA_ERR')

    if not isinstance(state, bool):
        return utils.rander('DATA_ERR')

    if email_id:
        update_dict = dict(
            host=host,
            title=title,
            sender=sender,
            password=password,
            receivers=json.dumps(receivers),
            state=state
        )
        email = models.MessageEmail.query.filter_by(id=email_id)
        if not email.first():
            return utils.rander('DATA_ERR', '此邮箱已不存在')

        try:
            email.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander('DATABASE_ERR')

        return utils.rander('OK')

    if not project_id:
        return utils.rander('DATA_ERR')

    try:
        add_email = models.MessageEmail(
            project_id=project_id,
            host=host,
            title=title,
            sender=sender,
            password=password,
            receivers=receivers,
            state=state
        )
        db.session.add(add_email)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


@api.route('/message/email/switch', methods=['POST', 'PUT'])
def update_message_email_switch():
    """
    更新 email 开关状态
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    state = body.get('state')
    email_id = body.get('id')

    if not email_id or not isinstance(state, bool):
        return utils.rander('DATA_ERR')

    update_dict = dict(
        state=state
    )
    try:
        email = models.MessageEmail.query.filter_by(id=email_id)
        if not email.first():
            return utils.rander('DATA_ERR', '此邮件不存在')
        email.update(update_dict)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')
