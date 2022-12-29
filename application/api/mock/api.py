# _author: Coke
# _date: 2022/12/29 13:55

from application.api import api
from application import utils, models, db
from flask import request

import logging
import json


@api.route('/mock/api/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_api_edit():
    """ 编辑/新增 接口信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    api_id = body.get('id')
    project_id = body.get('projectId')
    name = body.get('name')
    path = body.get('path')
    _body = body.get('body')

    if not all([project_id, name, path, _body]):
        return utils.rander(utils.DATA_ERR)

    project = models.Project.query.get(project_id)
    if not project:
        return utils.rander(utils.DATA_ERR, '项目不存在')

    try:
        _body = json.loads(_body)
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATA_ERR, 'JSON解析错误')
    else:
        _body = json.dumps(_body, ensure_ascii=False)

    api_info = models.Api.query.filter_by(path=path, project_id=project_id).first()
    if api_info and api_id != api_info.id:
        return utils.rander(utils.DATA_ERR, '此接口已存在')

    if api_id:
        api_info = models.Api.query.filter_by(id=api_id)

        if not api_info:
            return utils.rander(utils.DATA_ERR, '此接口不存在')

        update = dict(
            name=name,
            path=path,
            body=_body
        )
        try:
            api_info.update(update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    _api = models.Api(
        project_id=project_id,
        name=name,
        path=path,
        body=_body
    )
    try:
        db.session.add(_api)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/mock/api/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_api_list():
    """ 获取接口列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    path = body.get('path')
    name = body.get('name')

    if not all([project_id, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Api.name.like(f'%{name if name else ""}%'),
        models.Api.path.like(f'%{path if path else ""}%'),
        models.Api.project_id == project_id
    ]

    _api, total = utils.paginate(
        models.Api,
        page,
        size,
        filter_list=_query,
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(_api, total, page, size))


@api.route('/mock/api/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_api_info():
    """ 删除接口信息 """

    return utils.delete(models.Api, dict(id='id'))
