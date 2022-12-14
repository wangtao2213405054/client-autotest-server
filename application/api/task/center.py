# _author: Coke
# _date: 2022/12/13 13:53

from application.api import api
from application import utils, models, db, socketio
from flask import request

import logging


@api.route('/task/center/new', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def new_task_info():
    """ 新增一个任务 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    name = body.get('name')
    platform = body.get('platform')
    devices = body.get('devices')
    project_id = body.get('projectId')
    version = body.get('version')

    if not all([name, platform, project_id, version]):
        return utils.rander(utils.DATA_ERR)

    if devices and not all([isinstance(devices, list), len(devices) == 2]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task(
        name,
        platform,
        version,
        project_id,
        devices[1] if isinstance(devices, list) else None,
    )

    try:
        db.session.add(task)
        db.session.commit()
        socketio.emit('taskFree')
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/task/center/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_task_list():
    """ 获取当前任务列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    status = body.get('status')
    name = body.get('name')

    if not all([page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = {}

    if status:
        _query['status'] = status

    if name:
        _query['name'] = name

    task, total = utils.paginate(
        models.Task,
        page,
        size,
        filter_by=_query
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(task, total, page, size))


@api.route('/task/center/status', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def update_task_status():
    """ 更新任务状态 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('id')
    status = body.get('status')

    if not all([task_id, status, isinstance(status, int), status < 4]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=task_id)

    if not task.first():
        return utils.rander(utils.DATA_ERR, '此任务已不存在')

    try:
        task.update({'status': status})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
