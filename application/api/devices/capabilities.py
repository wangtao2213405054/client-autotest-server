# _author: Coke
# _date: 2022/11/29 16:20

from application.api import api
from application import db, models, utils
from flask import request

import logging
import json


@api.route('/devices/capabilities/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_capabilities_info():
    """ 编辑/新增 功能映射信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    capabilities_id = body.get('id')
    name = body.get('name')
    platform_name = body.get('platformName')
    mapping = body.get('mapping')

    if not mapping:
        return utils.rander(utils.DATA_ERR, '请添加映射信息后提交')

    if not all([name, platform_name, isinstance(mapping, list)]):
        return utils.rander(utils.DATA_ERR)

    if capabilities_id:
        update = {
            'name': name,
            'platform_name': platform_name,
            'mapping': json.dumps(mapping, ensure_ascii=False)
        }
        capabilities_info = models.Capabilities.query.filter_by(id=capabilities_id)
        if not capabilities_info.first():
            return utils.rander(utils.DATA_ERR, '此功能映射不存在')

        try:
            capabilities_info.update(update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    capabilities = models.Capabilities(
        name=name,
        platform_name=platform_name,
        mapping=mapping
    )
    try:
        db.session.add(capabilities)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/devices/capabilities/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_capabilities_list():
    """ 获取功能映射列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    page = body.get('page')
    size = body.get('pageSize')
    name = body.get('name')
    platform_name = body.get('platformName')

    if not all([page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Capabilities.name.like(f'%{name if name else ""}%')
    ]
    if platform_name:
        _query.append(models.Capabilities.platform_name == platform_name)

    capabilities_list, total = utils.paginate(
        models.Capabilities,
        page,
        size,
        filter_list=_query
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(capabilities_list, total, page, size))


@api.route('/devices/capabilities/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_capabilities_info():
    """ 删除功能映射信息 """

    return utils.delete(models.Capabilities, dict(id='id'))
