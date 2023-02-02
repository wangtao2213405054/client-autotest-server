# _author: Coke
# _date: 2022/12/13 13:53

from application.api import api
from application import utils, models, db, socketio
from flask import request, g
from sqlalchemy import or_

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
    project_id = body.get('projectId')
    url = body.get('url')
    environmental = body.get('environmental')

    version = body.get('version')
    priority = body.get('priority')
    _set = body.get('set')
    devices = body.get('devices')

    if not all([name, platform, project_id, environmental, url]):
        return utils.rander(utils.DATA_ERR)

    _environmental = models.Domain.query.filter_by(id=environmental).first()
    if not _environmental:
        return utils.rander(utils.DATA_ERR)

    if devices and not all([isinstance(devices, list), len(devices) == 2]):
        return utils.rander(utils.DATA_ERR)

    if _set and not isinstance(_set, list):
        return utils.rander(utils.DATA_ERR)

    query_case = [
        models.Case.project_id == project_id,
        models.Case.special == 0,
        models.Case.action == 1
    ]

    if _set:
        query_case.append(or_(models.Case.set_info.like(f'%{item},%') for item in _set))

    if version:
        _version = models.Version.query.filter_by(id=version).first()
        if not _version:
            return utils.rander(utils.DATA_ERR, '无此版本信息')

        _start_version = models.Version.query.filter(
            models.Version.project_id == project_id,
            _version.identify >= models.Version.identify
        ).all()
        _start_version = [item.id for item in _start_version]

        _end_version = models.Version.query.filter(
            models.Version.project_id == project_id,
            _version.identify < models.Version.identify
        ).all()
        _end_version = [item.id for item in _end_version]

        null = None
        query_case.append(or_(
            models.Case.start_version.in_(_start_version),
            models.Case.start_version == null
        ))
        query_case.append(or_(
            models.Case.end_version.in_(_end_version),
            models.Case.end_version == null
        ))

    case_info = models.Case.query.filter(*query_case).all()

    if not len(case_info):
        return utils.rander(utils.DATA_ERR, '筛选条件不存在用例')

    if isinstance(priority, bool):
        case_info = sorted(case_info, key=lambda x: x.priority, reverse=priority)
    cases = [item.id for item in case_info]

    task = models.Task(
        name,
        platform,
        environmental,
        url,
        cases,
        g.username,
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
    project_id = body.get('projectId')

    if not all([page, size, project_id]):
        return utils.rander(utils.DATA_ERR)

    _query = {
        'project_id': project_id
    }

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
    task_info = task.first()
    if not task_info:
        return utils.rander(utils.DATA_ERR, '此任务已不存在')

    try:
        task.update({'status': status})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('taskStatus', {'taskId': task_info.id, 'status': task_info.status})
    return utils.rander(utils.OK)
