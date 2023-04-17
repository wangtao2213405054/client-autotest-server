# _author: Coke
# _date: 2022/8/31 10:38

from application.api import api, swagger
from application import models, utils, db
from flask import request
from sqlalchemy import or_, and_

import logging
import json


@api.route('/conf/event/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('eventEdit.yaml')
def edit_event_info():
    """ 修改事件信息 """
    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    event_id = body.get('id')
    name = body.get('name')
    desc = body.get('desc')
    mapping = body.get('mapping')
    params = body.get('func')
    platform = body.get('platform')
    project_id = body.get('projectId')
    subset = body.get('subset')
    screenshot = body.get('screenshot')

    if not all([project_id, platform, mapping, desc, name, isinstance(subset, bool), isinstance(screenshot, bool)]):
        return utils.rander(utils.DATA_ERR)

    if event_id:
        update_dict = dict(
            name=name,
            desc=desc,
            mapping=mapping,
            params=json.dumps(params, ensure_ascii=False),
            platform=platform,
            project_id=project_id,
            subset=subset,
            screenshot=screenshot
        )
        try:
            event = models.Event.query.filter_by(id=event_id)
            if not event.first():
                return utils.rander(utils.DATA_ERR, '此事件不存在')

            event.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    event = models.Event(
        name=name,
        mapping=mapping,
        platform=platform,
        project_id=project_id,
        desc=desc,
        params=params,
        subset=subset,
        screenshot=screenshot
    )
    try:
        db.session.add(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.info(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/conf/event/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('eventDelete.yaml')
def delete_event_info():
    """ 删除事件信息 """

    return utils.delete(models.Event, dict(id='id'))


@api.route('conf/event/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('eventList.yaml')
def get_event_list():
    """ 获取事件列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    platform = body.get('platform')
    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    mapping = body.get('mapping')

    if not all([project_id, platform, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        or_(
            models.Event.platform == 'all',
            models.Event.platform == platform,
            and_(models.Event.platform == 'exclusive', models.Event.project_id == project_id)
        ),
        models.Event.name.like(f'%{name if name else ""}%'),
        models.Event.mapping.like(f'%{mapping if mapping else ""}%')
    ]

    try:
        event, total = utils.paginate(
            models.Event,
            page,
            size,
            _query
        )
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK, data=utils.paginate_structure(event, total, page, size))
