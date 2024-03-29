# _author: Coke
# _date: 2022/12/15 10:44

from application.api import api, swagger
from application import utils, db, models
from flask import request

import logging
import re


@api.route('/business/version/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('versionEdit.yaml')
def edit_version_info():
    """ 新增/编辑版本信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    version_id = body.get('id')
    name = body.get('name')
    identify = body.get('identify')
    desc = body.get('desc')

    if not all([project_id, name, identify, isinstance(identify, str)]):
        return utils.rander(utils.DATA_ERR)

    pattern = r'^\d+(?:\.\d+){2}$'
    if not re.match(pattern, identify):
        return utils.rander(utils.DATA_ERR)

    project = models.Project.query.filter_by(id=project_id).first()

    if not project:
        return utils.rander(utils.DATA_ERR, '项目不存在')

    if version_id:
        version = models.Version.query.filter_by(id=version_id)
        if not version.first():
            return utils.rander(utils.DATA_ERR, '版本信息不存在')

        update = {
            'name': name,
            'identify': identify,
            'desc': desc
        }

        try:
            version.update(update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    version = models.Version(
        name,
        identify,
        project_id,
        desc
    )
    try:
        db.session.add(version)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/business/version/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('versionList.yaml')
def get_version_list():
    """ 获取版本列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    name = body.get('name')
    page = body.get('page')
    size = body.get('pageSize')

    if not all([project_id, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Version.project_id == project_id,
        models.Version.name.like(f'%{name if name else ""}%')
    ]

    version, total = utils.paginate(
        models.Version,
        page,
        size,
        filter_list=_query
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(version, total, page, size))


@api.route('/business/version/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('versionDelete.yaml')
def delete_version_info():
    """ 删除版本信息 """

    return utils.delete(models.Version, dict(id='id'))
