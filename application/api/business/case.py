# _author: Coke
# _date: 2022/12/16 22:48

from application.api import api
from application import utils, db, models
from flask import request, g

import logging
import json


@api.route('/business/case/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_case_info():
    """ 编辑用例信息 """

    body = dict(request.get_json())

    if not body:
        return utils.rander(utils.BODY_ERR)

    case_id = body.get('id')
    project_id = body.get('projectId')
    name = body.get('name')
    desc = body.get('desc')
    special = body.get('special')
    action = body.get('action')
    start_version = body.get('startVersion')
    start_version = start_version if start_version else None
    end_version = body.get('endVersion')
    end_version = end_version if end_version else None
    set_info = body.get('setInfo')
    platform = body.get('platform')
    priority = body.get('priority')
    officer_list = body.get('officerList')
    module_list = body.get('moduleList')
    case_steps = body.get('caseSteps')
    case_steps = case_steps if case_steps else []
    pre_position = body.get('prePosition')
    pre_position = pre_position if pre_position else []
    post_position = body.get('postPosition')
    post_position = post_position if pre_position else []

    if not all([
        project_id, name, isinstance(special, bool), isinstance(action, bool), set_info, isinstance(set_info, list),
        platform, isinstance(platform, list), isinstance(priority, int), module_list, isinstance(module_list, list),
        case_steps, isinstance(case_steps, list)
    ]):
        return utils.rander(utils.DATA_ERR)

    business, module = module_list
    project = models.Project.query.filter_by(id=project_id).first()

    if not project:
        return utils.rander(utils.DATA_ERR, '项目信息不存在')

    _module = models.Folder.query.filter_by(id=module).first()

    if not _module:
        return utils.rander(utils.DATA_ERR, '模块信息不存在')

    if start_version and not models.Version.query.filter_by(id=start_version).first():
        return utils.rander(utils.DATA_ERR, '开始版本信息不存在')

    if end_version and not models.Version.query.filter_by(id=end_version).first():
        return utils.rander(utils.DATA_ERR, '结束版本信息不存在')

    try:
        utils.resolve(case_steps)
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATA_ERR, '用例步骤解析失败')

    if case_id:
        case = models.Case.query.filter_by(id=case_id)
        if not case.first():
            return utils.rander(utils.DATA_ERR, '用例不存在')

        update = dict(
            name=name,
            desc=desc,
            special=special,
            action=action,
            start_version=start_version,
            end_version=end_version,
            set_info=json.dumps(set_info),
            platform=json.dumps(platform),
            priority=priority,
            officer_list=json.dumps(officer_list),
            module=module,
            business=business,
            case_steps=json.dumps(case_steps, ensure_ascii=False),
            update_id=g.user_id,
            pre_position=json.dumps(pre_position),
            post_position=json.dumps(post_position),
        )
        try:
            case.update(update)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK, data=case.first().result)

    case = models.Case(
        project_id=project_id,
        name=name,
        desc=desc,
        special=special,
        action=action,
        start_version=start_version,
        end_version=end_version,
        set_info=set_info,
        platform=platform,
        priority=priority,
        officer_list=officer_list,
        module=module,
        business=business,
        case_steps=case_steps,
        create_id=g.user_id,
        update_id=g.user_id,
        pre_position=pre_position,
        post_position=post_position
    )
    try:
        db.session.add(case)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK, data=case.result)


@api.route('/business/case/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_case_list():
    """ 获取用例列表 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    project_id = body.get('projectId')
    page = body.get('page')
    size = body.get('pageSize')
    folder_id = body.get('folderId')
    folder_id = folder_id if folder_id else []
    name = body.get('name')
    special = body.get('special')
    action = body.get('action')

    if not all([page, size, project_id]):
        return utils.rander(utils.DATA_ERR)

    if folder_id and not all([isinstance(folder_id, list), len(folder_id) == 2]):
        return utils.rander(utils.DATA_ERR)

    _query = [
        models.Case.project_id == project_id,
        models.Case.name.like(f'%{name if name else ""}%')
    ]

    if isinstance(special, bool):
        _query.append(models.Case.special == special)

    if isinstance(action, bool):
        _query.append(models.Case.action == action)

    if folder_id:
        business, module = folder_id
        _query.append(models.Case.module == module if business else models.Case.business == module)

    case, total = utils.paginate(
        models.Case,
        page,
        size,
        filter_list=_query,
        source=False
    )

    case_dict_list = []
    for item in case:
        items = item.result
        create_name = query_name(item.create_id)
        update_name = query_name(item.update_id)
        items['createName'] = create_name.name if create_name else ''
        items['updateName'] = update_name.name if update_name else ''
        case_dict_list.append(items)

    return utils.rander(utils.OK, data=utils.paginate_structure(case_dict_list, total, page, size))


def query_name(_id):
    """ 通过id查询用户信息 """
    return models.User.query.filter_by(id=_id).first()


@api.route('/business/case/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_case_info():
    """ 删除用例信息 """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    case_id = body.get('id')

    if not case_id:
        return utils.rander(utils.DATA_ERR)

    case = models.Case.query.filter_by(id=case_id)

    if not case.first():
        return utils.rander(utils.DATA_ERR, '用例不存在')

    try:
        case.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('/business/case/info', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_case_info():
    """ 通过ID获取用例详情(执行机使用) """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    case_id = body.get('id')

    case = models.Case.query.filter_by(id=case_id).first()

    if not case:
        return utils.rander(utils.DATA_ERR, '用例不存在')

    case_info = case.result
    case_info['caseSteps'] = utils.resolve(case_info['caseSteps'])
    case_info['startVersionIdentify'] = models.Version.query.filter_by(id=case_info['startVersion']).first().identify
    case_info['endVersionIdentify'] = models.Version.query.filter_by(id=case_info['startVersion']).first().identify

    return utils.rander(utils.OK, data=case_info)
