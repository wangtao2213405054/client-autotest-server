# _author: Coke
# _date: 2022/12/15 10:44

from application.api import api
from application import utils, db, models
from flask import request

import logging
import json


@api.route('/business/set/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_set_info():
    """ 新增/编辑集合信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    set_id = body.get('id')
    name = body.get('name')
    special = body.get('special')
    desc = body.get('desc')
    custom_set = body.get('customSet')
    custom_set = custom_set if custom_set else []

    if not all([project_id, name, isinstance(special, bool), isinstance(custom_set, list)]):
        return utils.rander(utils.DATA_ERR)

    if special and not custom_set:
        return utils.rander(utils.DATA_ERR, '特殊集合请选择测试用例')

    for item in custom_set:
        if not isinstance(item, list) or len(item) != 3:
            return utils.rander(utils.DATA_ERR)

    project = models.Project.query.filter_by(id=project_id).first()

    if not project:
        return utils.rander(utils.DATA_ERR, '项目不存在')

    if set_id:
        _set = models.Set.query.filter_by(id=set_id)
        if not _set.first():
            return utils.rander(utils.DATA_ERR, '集合不存在')

        update = dict(
            name=name,
            special=special,
            desc=desc,
            custom_set=json.dumps(custom_set, ensure_ascii=False)
        )
        try:
            _set.update(update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    _set = models.Set(
        name,
        special,
        project_id,
        desc,
        custom_set
    )
    try:
        db.session.add(_set)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/business/set/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_set_list():
    """ 获取集合列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    special = body.get('special')

    if not all([page, size, project_id]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Set.project_id == project_id,
        models.Set.name.like(f'%{name if name else ""}%')
    ]
    if isinstance(special, bool):
        _query.append(models.Set.special == special)

    _set, total = utils.paginate(
        models.Set,
        page,
        size,
        filter_list=_query
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(_set, total, page, size))


@api.route('/business/set/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_set_info():
    """ 删除集合信息 """

    return utils.delete(models.Set, dict(id='id'))
