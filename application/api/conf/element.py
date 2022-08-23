# _author: Coke
# _date: 2022/8/23 13:41


from application.api import api
from application import utils, db, models
from flask import request

import logging
import json


@api.route('/conf/element/list', methods=['GET', 'POST'])
def get_element_list():
    """
    获取元素列表
    :return:
    """

    body = request.get_json(silent=True)

    if not body:
        return utils.rander('BODY_ERR')

    platform = body.get('platform')
    page = body.get('page')
    size = body.get('size')

    if not all([page, size]):
        return utils.rander('DATA_ERR')

    query_list = [
        models.Element.platform.like(f'%{platform if platform else ""}%')
    ]

    data, total = utils.paginate(
        models.Element,
        page,
        size,
        filter_list=query_list
    )
    element_dict_list = []
    for items in data:
        element_dict_list.append(items.to_dict())

    return utils.rander('OK', data=utils.paginate_structure(element_dict_list, total, page, size))


@api.route('/conf/element/edit', methods=['POST', 'PUT'])
def edit_element_info():
    """
    新增/修改元素信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    element_id = body.get('id')
    name = body.get('name')
    label = body.get('label')
    desc = body.get('desc')
    platform = body.get('platform')

    if not all([name, label, platform]):
        return utils.rander('DATA_ERR')

    if element_id:
        update_dict = dict(
            name=name,
            label=label,
            desc=desc,
            platform=json.dumps(platform, ensure_ascii=False)
        )
        try:
            element = models.Element.query.filter_by(id=element_id)

            if not element.first():
                return utils.rander('DATA_ERR', '此元素已不存在')

            element.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander('DATABASE_ERR', '123')

        return utils.rander('OK')

    element = models.Element(
        name,
        label,
        desc,
        platform
    )
    try:
        db.session.add(element)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')


@api.route('conf/element/delete', methods=['POST', 'DELETE'])
def delete_element_info():
    """
    删除元素信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander('BODY_ERR')

    element_id = body.get('id')

    if not element_id:
        return utils.rander('DATA_ERR')

    try:
        element = models.Element.query.filter_by(id=element_id)
        if not element.first():
            return utils.rander('DATA_ERR', '此元素已不存在')
        element.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander('DATABASE_ERR')

    return utils.rander('OK')
