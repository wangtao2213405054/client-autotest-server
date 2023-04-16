# _author: Coke
# _date: 2022/12/29 13:55

from application.api import api, swagger
from application import utils, models, db
from flask import request

import logging


@api.route('/mock/domain/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
@swagger('domainEdit.yaml')
def edit_domain_info():
    """ 编辑/新增域名信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    domain_id = body.get('id')
    name = body.get('name')
    protocol = body.get('protocol')
    port = body.get('port')
    domain = body.get('domain')

    if not all([port, protocol, domain, name, project_id]):
        return utils.rander(utils.DATA_ERR)

    project = models.Project.query.filter_by(id=project_id).first()

    if not project:
        return utils.rander(utils.DATA_ERR, '项目不存在')

    domain_info = models.Domain.query.filter_by(project_id=project_id, domain=domain).first()

    if domain_info and domain_id != domain_info.id:
        return utils.rander(utils.DATA_ERR, '域名已存在')

    if domain_id:
        _domain = models.Domain.query.filter_by(id=domain_id)

        if not _domain.first():
            return utils.rander(utils.DATA_ERR, '此域名不存在')

        update = dict(
            name=name,
            protocol=protocol,
            port=port,
            domain=domain
        )
        try:
            _domain.update(update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    _domain = models.Domain(
        project_id=project_id,
        name=name,
        protocol=protocol,
        port=port,
        domain=domain
    )
    try:
        db.session.add(_domain)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/mock/domain/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
@swagger('domainList.yaml')
def get_domain_list():
    """ 获取域名列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    domain = body.get('domain')
    name = body.get('name')
    protocol = body.get('protocol')

    if not all([project_id, page, size]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Domain.project_id == project_id,
        models.Domain.name.like(f'%{name if name else ""}%'),
        models.Domain.domain.like(f'%{domain if domain else ""}%')
    ]

    if protocol:
        _query.append(models.Domain.protocol == protocol)

    _domain, total = utils.paginate(
        models.Domain,
        page,
        size,
        filter_list=_query,
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(_domain, total, page, size))


@api.route('/mock/domain/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
@swagger('domainDelete.yaml')
def delete_domain_info():
    """ 删除域名信息 """

    return utils.delete(models.Domain, dict(id='id'))
