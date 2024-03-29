# _author: Coke
# _date: 2022/11/28 11:35

from application import utils, models, db, ws, socketio
from application.api import api, swagger
from flask import request

import logging
import json


def update_context(master_id, operation=True):
    """ 更新控制设备当前绑定数量 """

    master = models.Master.query.filter_by(id=master_id)
    master_info = master.first()
    if not master_info:
        return

    number = master_info.context + 1 if operation else master_info.context - 1
    master.update({
        'context': number if number >= 0 else 0
    })


@api.route('/devices/worker/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('workerEdit.yaml')
def edit_worker_info():
    """ 编辑执行器信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    worker_id = body.get('id')
    name = body.get('name')
    desc = body.get('desc')
    blocker = body.get('blocker')
    switch = body.get('switch')
    log = body.get('logging')
    mapping = body.get('mapping')
    master = body.get('master')

    if not all([name, mapping, master, log, blocker, isinstance(switch, bool)]):
        return utils.rander(utils.DATA_ERR)

    try:
        mapping = json.loads(mapping)
        required = ['platformName', 'mockProxy']
        for item in required:
            if item not in mapping:
                return utils.rander(utils.DATA_ERR, f'映射中必须包含 {item}')
    except (Exception, ):
        return utils.rander(utils.DATA_ERR, '映射解析错误')

    master_info = models.Master.query.filter_by(id=master).first()

    if not master_info:
        return utils.rander(utils.DATA_ERR, '控制器已不存在')

    if master != master_info.id and master_info.context >= master_info.max_context:
        return utils.rander(utils.DATA_ERR, '控制器已达最大绑定进程数')

    if worker_id:
        update = {
            'name': name,
            'desc': desc,
            'mapping': json.dumps(mapping, ensure_ascii=False),
            'master': master,
            'blocker': blocker,
            'switch': switch,
            'log': log
        }

        worker_info = models.Worker.query.filter_by(id=worker_id)
        worker = worker_info.first()
        if not worker:
            return utils.rander(utils.DATA_ERR, '此设备已不存在')

        try:
            update_context(worker.master, False)
            worker_info.update(update)
            update_context(master)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

    else:
        worker = models.Worker(name, desc, mapping, master, blocker, switch, log)

        try:
            db.session.add(worker)
            update_context(master)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

    result = utils.socket_call(master_info.key, 'workerDeviceEdit', worker.result)
    if not result:
        return utils.rander(utils.SOCKET_ERR)

    return utils.rander(utils.OK)


@api.route('/devices/worker/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('workerList.yaml')
def get_worker_list():
    """ 获取执行设备列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    master = body.get('master')
    status = body.get('status')

    if not all([page, size]):
        return utils.rander(utils.DATA_ERR)

    # 数据过滤
    query_info = [
        models.Worker.name.like(f'%{name if name else ""}%'),
    ]
    if status is not None:
        query_info.append(models.Worker.status == status)

    if master:
        query_info.append(models.Worker.master == master)

    worker_list, total = utils.paginate(
        models.Worker,
        page,
        size,
        filter_list=query_info,
        source=False
    )

    worker_dict_list = []
    for item in worker_list:
        master_info = models.Master.query.filter_by(id=item.master).first()
        if not master_info or master_info.key not in ws.online_server:
            item.status = 4
        worker_dict_list.append(item.result)

    return utils.rander(utils.OK, data=utils.paginate_structure(worker_dict_list, total, page, size))


@api.route('/devices/worker/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('workerDelete.yaml')
def delete_worker_info():
    """ 删除执行设备信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    worker_id = body.get('id')
    master_id = body.get('master')

    if not all([worker_id, master_id]):
        return utils.rander(utils.DATA_ERR)

    worker = models.Worker.query.filter_by(id=worker_id)
    worker_info = worker.first()
    if not worker_info:
        return utils.rander(utils.DATA_ERR, '设备不存在')

    try:
        worker.delete()
        update_context(master_id, False)
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)
    else:
        master_info = models.Master.query.filter_by(id=worker_info.master).first()
        result = utils.socket_call(master_info.key, 'workerDeviceDelete', {'id': worker_info.id})
        if not result:
            return utils.rander(utils.SOCKET_ERR)

        db.session.commit()

    return utils.rander(utils.OK)


@api.route('/devices/worker/switch', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('workerSwitch.yaml')
def edit_worker_switch_status():
    """ 开启/关闭执行机任务轮训 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    worker_id = body.get('id')
    switch = body.get('switch')
    kill = body.get('kill')

    if not all([worker_id, isinstance(switch, bool)]):
        return utils.rander(utils.DATA_ERR)

    worker = models.Worker.query.filter_by(id=worker_id)
    worker_info = worker.first()

    if not worker_info:
        return utils.rander(utils.DATA_ERR, '设备不存在')

    master = models.Master.query.filter_by(id=worker_info.master)
    master_info = master.first()

    result = utils.socket_call(
        master_info.key,
        'workerTaskSwitch',
        {'switch': switch, 'kill': kill, 'workerId': worker_id}
    )

    if not result:
        return utils.rander(utils.SOCKET_ERR)

    try:
        worker.update({'switch': switch, 'status': 0 if switch else 3})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/devices/worker/status', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('workerStatus.yaml')
def edit_worker_status():
    """ 修改工作机的设备状态 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    worker_id = body.get('id')
    status = body.get('status')  # 0 成功 1任务中 2 异常
    cause = body.get('cause')
    cause = cause if cause else None
    if not all([worker_id, isinstance(status, int), status < 3]):
        return utils.rander(utils.DATA_ERR)

    worker = models.Worker.query.filter_by(id=worker_id)

    if not worker.first():
        return utils.rander(utils.DATA_ERR, '设备不存在')

    update = {
        'status': status,
        'cause': cause,
    }
    if status == 0:
        update['actual'] = worker.first().actual + 1

    try:
        worker.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    socketio.emit('workerStatus', {'id': worker_id, 'status': status, 'cause': cause})

    return utils.rander(utils.OK)
