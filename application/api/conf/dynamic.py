# _author: Coke
# _date: 2023/8/30 21:33

from application.api import api
from application import utils, db, models
from sqlalchemy import or_
from flask import request

import logging
import json


@api.route('/conf/dynamic/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_dynamic_list():
    """
    获取动态元素列表
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    keyword = body.get('keyword')
    keyword = keyword if keyword else ""

    if not all([page, size]):
        return utils.rander(utils.DATA_ERR)

    query_list = [
        or_(models.DynamicElement.name.like(f'%{keyword}%'), models.DynamicElement.expression.like(f'%{keyword}%'))
    ]

    data, total = utils.paginate(
        models.DynamicElement,
        page,
        size,
        filter_list=query_list
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(data, total, page, size))


@api.route('/conf/dynamic/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_dynamic_info():
    """
    新增/修改动态元素
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    dynamic_id = body.get('id')
    name = body.get('name')
    expression = body.get('expression')
    data_type = body.get('type')
    element = body.get('element')
    placeholder = body.get('placeholder')
    options = body.get('options')
    options = options if isinstance(options, list) else []

    if not all([name, expression, element]):
        return utils.rander(utils.DATA_ERR)

    if dynamic_id:
        dynamic = models.DynamicElement.query.filter_by(id=dynamic_id)

        if not dynamic.first():
            return utils.rander(utils.DATA_ERR, '此字典已不存在')

        update_dict = dict(
            name=name,
            expression=expression,
            data_type=data_type,
            element=element,
            placeholder=placeholder,
            options=json.dumps(options, ensure_ascii=False)
        )

        try:
            dynamic.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    dynamic = models.DynamicElement(placeholder, element, data_type, name, expression, options)
    try:
        db.session.add(dynamic)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('conf/dynamic/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_dynamic_info():
    """
    删除动态元素
    :return:
    """

    return utils.delete(models.DynamicElement, dict(id='id'))
