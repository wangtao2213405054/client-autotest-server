# _author: Coke
# _date: 2022/12/14 15:01

from application.api import api
from application import utils, models, db, socketio
from flask import request

import logging


@api.route('/task/report/new', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def new_task_report():
    """ 添加一个测试报告信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('id')
    name = body.get('name')
    desc = body.get('desc')
    status = body.get('status')

    if not all([task_id, name, isinstance(status, int)]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=task_id).first()
    if not task:
        return utils.rander(utils.DATA_ERR, '任务不存在')

    report = models.Report(
        name, desc, task_id, status
    )
    try:
        db.session.add(report)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('taskReportInfo', report.to_dict, to=f'taskReport{task_id}')
    return utils.rander(utils.OK)


@api.route('/task/report/start', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def start_task_info():
    """ 任务开始执行时调用 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('id')
    count = body.get('count')

    if not all([task_id, count]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=task_id)
    task_info = task.first()
    if not task_info:
        return utils.rander(utils.DATA_ERR, '任务不存在')

    try:
        task.update({'status': 1, 'count': count})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('taskStatus', {'taskId': task_info.id, 'status': task_info.status})
    return utils.rander(utils.OK)


@api.route('/task/report/end', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def end_report_info():
    """ 测试结束时调用 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('id')
    status = body.get('status')

    if not all([task_id, status]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=task_id)
    task_info = task.first()
    if not task_info:
        return utils.rander(utils.DATA_ERR, '任务不存在')

    try:
        task.update({'status': status})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('taskStatus', {'taskId': task_info.id, 'status': task_info.status})
    return utils.rander(utils.OK)


@api.route('/task/report/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_report_list():
    """ 获取任务的测试报告列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('taskId')
    page = body.get('page')
    size = body.get('pageSize')

    if not all([task_id, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Report.task_id == task_id
    ]

    report, total = utils.paginate(
        models.Report,
        page,
        size,
        filter_list=_query
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(report, total, page, size))
