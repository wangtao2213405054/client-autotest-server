# _author: Coke
# _date: 2022/12/29 13:55

from application.api import api, swagger
from application import utils, models, db
from sqlalchemy import or_
from flask import request

import logging
import json


@api.route('/mock/api/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('apiEdit.yaml')
def edit_api_edit():
    """ 编辑/新增 接口信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    api_id = body.get('id')
    project_id = body.get('projectId')
    name = body.get('name')
    path = body.get('path')
    overall = body.get('overall')
    record_request = body.get('recordRequest')
    record_response = body.get('recordResponse')
    breakpoint_request = body.get('breakpointRequest')
    breakpoint_response = body.get('breakpointResponse')
    _request = body.get('request')
    _response = body.get('response')

    if not all([
        project_id,
        name,
        path,
        (breakpoint_request and _request) or (not breakpoint_request and not _request),
        (breakpoint_response and _response) or (not breakpoint_response and not _response),
    ]):
        return utils.rander(utils.DATA_ERR)

    project = models.Project.query.get(project_id)
    if not project:
        return utils.rander(utils.DATA_ERR, '项目不存在')

    try:
        _request = json.loads(_request) if _request else ""
        _response = json.loads(_response) if _response else ""
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATA_ERR, 'JSON解析错误')
    else:
        _request = json.dumps(_request, ensure_ascii=False) if _request else ""
        _response = json.dumps(_response, ensure_ascii=False) if _response else ""

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
            overall=overall,
            recordRequest=record_request,
            recordResponse=record_response,
            breakpointRequest=breakpoint_request,
            breakpointResponse=breakpoint_response,
            request=_request,
            response=_response,
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
        overall=overall,
        record_request=record_request,
        record_response=record_response,
        breakpoint_request=breakpoint_request,
        breakpoint_response=breakpoint_response,
        request=_request,
        response=_response
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
@swagger('apiList.yaml')
def get_api_list():
    """ 获取接口列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    keyword = body.get('keyword')
    keyword = keyword if keyword else ""

    if not all([project_id, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        or_(models.Api.name.like(f'%{keyword}%'), models.Api.path.like(f'%{keyword}%')),
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
@swagger('apiDelete.yaml')
def delete_api_info():
    """ 删除接口信息 """

    return utils.delete(models.Api, dict(id='id'))
