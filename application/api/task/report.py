# _author: Coke
# _date: 2022/12/14 15:01

from application.api import api
from application import utils, models, db, socketio
from flask import request

import logging
import json


@api.route('/task/report/new', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def new_task_report():
    """ 添加一个测试报告信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    task_id = body.get('id')
    case_id = body.get('caseId')
    name = body.get('name')
    details = body.get('details')
    module = body.get('module')
    set_list = body.get('setList')
    priority = body.get('priority')
    output = body.get('output')
    images = body.get('images')
    images = images if images else []
    status = body.get('status')
    error_step = body.get('errorStep')
    error_info = body.get('errorInfo')
    error_details = body.get('errorDetails')
    gif = body.get('gif')
    start_time = body.get('startTime')
    stop_time = body.get('stopTime')
    duration = body.get('duration')

    if not all([
        task_id,
        case_id,
        name,
        module,
        set_list,
        priority,
        start_time,
        stop_time,
        duration,
        isinstance(status, int)
    ]):
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=task_id)
    task_info = task.first()
    if not task_info:
        return utils.rander(utils.DATA_ERR, '任务不存在')

    task_dict = {}
    if status == 1:
        task_dict['pass_case'] = task_info.pass_case + 1
    else:
        task_dict['fail_case'] = task_info.fail_case + 1
    report = models.Report(
        name=name,
        task_id=task_id,
        status=status,
        case_id=case_id,
        details=details,
        module=module,
        set_list=set_list,
        priority=priority,
        output=output,
        images=images,
        error_step=error_step,
        error_info=error_info,
        error_details=error_details,
        gif=gif,
        start_time=start_time,
        stop_time=stop_time,
        duration=duration
    )
    try:
        db.session.add(report)
        task.update(task_dict)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    _run_info = {
        'taskId': task_info.id,
        'passCase': task_info.pass_case,
        'failCase': task_info.fail_case,
        'percentage': round((task_info.pass_case + task_info.fail_case) / len(json.loads(task_info.cases)) * 100, 2),
        'taskStatus': task_info.status
    }
    socketio.emit('taskRunningStatus', _run_info)
    _run_info.update(report.result)
    socketio.emit('taskReportInfo', _run_info, to=f'taskReport{task_id}')
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
