# _author: Coke
# _date: 2022/11/18 15:26

from application import utils, db, models, ws
from application.api import api
from flask import request, g
from sqlalchemy import or_

import logging
import json

lock = utils.Lock()


def _structure(data=None, switch=False):
    """ 任务数据结构 """
    return utils.rander(utils.OK, data=dict(free=switch, task=data))


@api.route('/task/master/get', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_task_info():
    """ master控制机获取任务信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    free = body.get('free')

    if not all([free, isinstance(free, list)]):
        return utils.rander(utils.DATA_ERR)

    # 控制机信息
    master = models.Master.query.filter_by(key=g.user_id).first()

    # 如果控制机开关和socket在线状态不为真则返回
    if not master.status or master.key not in ws.online_server:
        return _structure()

    _lock = lock.acquire()
    if not _lock:
        return _structure(switch=True)

    # 获取/过滤可执行任务的执行机
    worker = models.Worker.query.filter(
        or_(*[models.Worker.id == item for item in free]),
        models.Worker.switch == 1
    ).all()

    _task_dict_list = []
    for item in worker:
        # 查询条件
        _query = [
            models.Task.platform == json.loads(item.mapping).get('platformName'),
            or_(models.Task.devices == {}.get(''), models.Task.devices == item.id),
            models.Task.sign == 0
        ]
        # 如果控制机所属于某个项目则添加过滤条件
        if master.project_id:
            _query.append(models.Task.project_id == master.project_id)

        task = models.Task.query.filter(*_query).first()
        # 无匹配任务后跳过循环
        if not task:
            continue

        _task_info = task.result
        _task_info['power'] = item.id
        _task_dict_list.append(_task_info)

        # 修改任务状态
        try:
            models.Task.query.filter_by(id=task.id).update({'sign': True})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

    # 查询当前控制机是否还有可执行的任务
    _worker = models.Worker.query.filter_by(master=master.id, switch=True).all()
    _free_query = [
        # 当前控制机的所有平台
        or_(*[models.Task.platform == json.loads(item.mapping).get('platformName') for item in _worker]),
        models.Task.sign == 0,  # 可执行的任务
        # # 未指定设备或指定当前控制机的执行机
        or_(models.Task.devices == {}.get(''), *[models.Task.devices == item.id for item in _worker])
    ]
    if master.project_id:
        # 当前控制机所绑定的项目
        _free_query.append(models.Task.project_id == master.project_id)
    _free = models.Task.query.filter(*_free_query).first()

    lock.release()  # 释放锁
    return _structure(_task_dict_list, True if _free else False)


@api.route('/task/master/sign', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_task_sign():
    """ 将任务的标记置为False """

    _id = utils.query_id()

    if not _id:
        return utils.rander(utils.DATA_ERR)

    task = models.Task.query.filter_by(id=_id)

    if not task.first():
        return utils.rander(utils.DATA_ERR, '此任务已不存在')

    try:
        task.update({'sign': False})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)
