# _author: Coke
# _date: 2022/11/28 11:35

from application import utils, db, models, ws
from application.api import api
from flask import request, g

import logging
import uuid


@api.route('/devices/master/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_master_info():
    """ 新增/修改 控制设备信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    master_id = body.get('id')
    name = body.get('name')
    max_context = body.get('maxContext')
    desc = body.get('desc')
    role = body.get('role')
    project_id = body.get('projectId')
    status = body.get('status')
    log = body.get('logging')
    project_id = project_id if project_id else None

    if not all([name, max_context, role, log, isinstance(status, bool)]):
        return utils.rander(utils.DATA_ERR)

    # 验证角色信息
    role_info = models.Role.query.get(role)
    if not role_info:
        return utils.rander(utils.DATA_ERR, '角色信息不存在')

    # 验证项目
    if project_id and not models.Project.query.get(project_id):
        return utils.rander(utils.DATA_ERR, '项目信息不存在')

    if master_id:
        master_info = models.Master.query.filter_by(id=master_id)
        master = master_info.first()
        if not master:
            return utils.rander(utils.DATA_ERR, '此信息已不存在')

        update = {
            'name': name,
            'max_context': max_context,
            'desc': desc,
            'role': role,
            'project_id': project_id,
            'status': status,
            'log': log
        }
        try:
            master_info.update(update)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander(utils.DATABASE_ERR)
        else:
            result = utils.socket_call(master.key, 'masterDeviceEdit', master.result)
            if not result:
                return utils.rander(utils.SOCKET_ERR)

        return utils.rander(utils.OK)

    did = uuid.uuid1().hex
    token = utils.create_token(True, username=name, user_id=did)
    master = models.Master(
        name=name,
        max_context=max_context,
        desc=desc,
        key=did,
        token=token,
        role=role,
        project_id=project_id,
        status=status,
        log=log
    )
    try:
        db.session.add(master)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK, data=token)


@api.route('/devices/master/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_master_list():
    """ 获取控制设备列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    project_id = body.get('projectId')
    status = body.get('status')

    if not all([page, size]):
        return utils.rander(utils.DATA_ERR)

    # 数据过滤
    query_info = [
        models.Master.name.like(f'%{name if name else ""}%'),
    ]
    if isinstance(status, bool):
        query_info.append(models.Master.status == status)

    if project_id:
        query_info.append(models.Master.project_id == project_id)

    master_list, total = utils.paginate(
        models.Master,
        page,
        size,
        filter_list=query_info,
        source=False
    )

    # 获取设备在线状态
    master_dict_list = []
    for item in master_list:
        items = item.result
        items['online'] = item.key in ws.online_server
        master_dict_list.append(items)

    return utils.rander(utils.OK, data=utils.paginate_structure(master_dict_list, total, page, size))


@api.route('/devices/master/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_master_info():
    """ 删除执行的设备信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    master_id = body.get('id')

    if not master_id:
        return utils.rander(utils.DATA_ERR)

    try:
        master = models.Master.query.filter_by(id=master_id)
        master_info = master.first()
        master.delete()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander(utils.DATABASE_ERR)
    else:
        result = utils.socket_call(master_info.key, 'masterDeviceDelete')
        if not result:
            return utils.rander(utils.SOCKET_ERR)

        db.session.commit()

    return utils.rander(utils.OK)


@api.route('/devices/master/status', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_master_status():
    """ 修改控制设备当前状态 """

    body: dict = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    master_id = body.get('id')
    status = body.get('status')

    if not all([master_id, isinstance(status, bool)]):
        return utils.rander(utils.DATA_ERR)

    master_info = models.Master.query.filter_by(id=master_id)
    master = master_info.first()
    if not master:
        return utils.rander(utils.DATA_ERR, '此设备已不存在')

    result = utils.socket_call(master.key, 'masterTaskSwitch', {'switch': status})
    if not result:
        return utils.rander(utils.SOCKET_ERR)

    update = {
        'status': status
    }
    try:
        master_info.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/devices/master/info', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_master_info():
    """ 获取当前设备信息 """

    master_info = models.Master.query.filter_by(key=g.user_id).first()

    if not master_info:
        return utils.rander(utils.DATA_ERR, '此设备不存在')

    return utils.rander(utils.OK, data=master_info.result)


@api.route('/devices/master/socket', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def join_master_room():
    """ 通过控制机ID加入房间 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    master_id = body.get('id')

    master_info = models.Master.query.filter_by(id=master_id).first()

    if not master_info:
        return utils.rander(utils.DATA_ERR, '设备不存在')

    user_id = master_info.key
    if user_id not in ws.online_server or not ws.session_maps.get(user_id):
        return utils.rander(utils.DATA_ERR, '设备不在线')

    if not ws.session_maps.get(g.user_id) or g.user_id not in ws.online_server:
        return utils.rander(utils.SOCKET_ERR, 'Socket 链接断开, 请刷新页面后尝试')

    return utils.rander(utils.OK, data=f'systemRoom{ws.session_maps.get(user_id)}')
