# _author: Coke
# _date: 2022/11/28 11:35

from application import utils, db, models
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
        return utils.rander('BODY_ERR')

    master_id = body.get('id')
    name = body.get('name')
    max_context = body.get('maxContext')
    desc = body.get('desc')
    role = body.get('role')
    project_id = body.get('projectId')
    status = body.get('status')
    project_id = project_id if project_id else None

    if not all([name, max_context, role]) or not isinstance(status, bool):
        return utils.rander('DATA_ERR')

    # 验证角色信息
    role_info = models.Role.query.get(role)
    if not role_info:
        return utils.rander('DATA_ERR', '角色信息不存在')

    # 验证项目
    if project_id and not models.Project.query.get(project_id):
        return utils.rander('DATA_ERR', '项目信息不存在')

    print(project_id, 'this is test ~')
    if master_id:
        master_info = models.Master.query.filter_by(id=master_id)
        if not master_info.first():
            return utils.rander('DATA_ERR', '此信息已不存在')

        update = {
            'name': name,
            'max_context': max_context,
            'desc': desc,
            'role': role,
            'project_id': project_id,
            'status': status
        }
        try:
            master_info.update(update)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return utils.rander('DATABASE_ERR')

        return utils.rander('OK')

    udid = uuid.uuid1().hex
    token = utils.create_token(True, user_name=name, user_id=udid)
    master = models.Master(
        name=name,
        max_context=max_context,
        desc=desc,
        key=udid,
        token=token,
        role=role,
        project_id=project_id,
        status=status
    )
    try:
        db.session.add(master)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK', data=token)


@api.route('/devices/master/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_master_list():
    """ 获取控制设备列表 """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    project_id = body.get('projectId')
    status = body.get('status')

    if not all([page, size]):
        return utils.rander('DATA_ERR')

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
        filter_list=query_info
    )

    return utils.rander('OK', data=utils.paginate_structure(master_list, total, page, size))


@api.route('/devices/master/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_master_info():
    """ 删除执行的设备信息 """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    master_id = body.get('id')

    if not master_id:
        return utils.rander('DATA_ERR')

    try:
        models.Master.query.filter_by(id=master_id).delete()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


@api.route('/devices/master/status', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_master_status():
    """ 修改控制设备当前状态 """

    body: dict = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    master_id = body.get('id')
    status = body.get('status')

    if not master_id or not isinstance(status, bool):
        return utils.rander('DATA_ERR')

    master_info = models.Master.query.filter_by(id=master_id)
    if not master_info.first():
        return utils.rander('DATA_ERR', '此设备已不存在')

    update = {
        'status': status
    }
    try:
        master_info.update(update)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


@api.route('/devices/master/info', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_master_info():
    """ 获取当前设备信息 """

    master_info = models.Master.query.filter_by(key=g.user_id).first()

    if not master_info:
        return utils.rander('DATA_ERR', '此信息不存在')

    return utils.rander('OK', data=master_info.to_dict)
