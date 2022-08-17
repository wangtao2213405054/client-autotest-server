# _author: Coke
# _date: 2022/8/16 15:52

from application.api import api
from application import utils, db, models
from flask import request
from .common import message_switch

import logging
import json


@api.route('/message/robot/info', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_message_robot_info():
    """
    获取机器人配置
    :return:
    """
    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    app = body.get('app')
    project_id = body.get('projectId')

    if not all([app, project_id]):
        return utils.rander('DATA_ERR')

    robot = models.MessageRobot.query.filter_by(project_id=project_id, app=app).first()

    if not robot:
        default = dict(
            id=None,
            projectId=project_id,
            app=app,
            tokens=[{'token': None, 'sign': None}],
            atAll='no',
            atMobile=[],
            status=False
        )
        return utils.rander('OK', data=default)

    return utils.rander('OK', data=robot.to_dict())


@api.route('/message/robot/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_message_robot_info():
    """
    新增/修改机器人配置
    :return:
    """
    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    robot_id = body.get('id')
    project_id = body.get('projectId')
    app = body.get('app')
    tokens = body.get('tokens')
    at_all = body.get('atAll')
    at_mobile = body.get('atMobile')
    status = body.get('status')

    if not all([at_all, tokens, app]):
        return utils.rander('DATA_ERR')
    if status is None:
        status = False

    if robot_id:
        update_dict = dict(
            tokens=json.dumps(tokens, ensure_ascii=False),
            at_all=at_all,
            at_mobile=json.dumps(at_mobile, ensure_ascii=False),
            status=status
        )
        robot = models.MessageRobot.query.filter_by(id=robot_id)
        if not robot.first():
            return utils.rander('DATA_ERR', '此机器人已不存在')

        try:
            robot.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander('DATABASE_ERR')

        return utils.rander('OK')

    if not project_id:
        return utils.rander('DATA_ERR')

    try:
        add_robot = models.MessageRobot(
            project_id=project_id,
            app=app,
            tokens=tokens,
            at_all=at_all,
            at_mobile=at_mobile,
            status=status
        )
        db.session.add(add_robot)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


@api.route('/message/robot/switch', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_message_robot_switch():
    """
    修改机器人开关
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    robot_id = body.get('id')
    status = body.get('status')

    if not robot_id or not isinstance(status, bool):
        return utils.rander('DATA_ERR')

    update_dict = dict(
        status=status
    )
    return message_switch(
        robot_id,
        update_dict,
        '此机器人不存在',
        models.MessageRobot
    )
