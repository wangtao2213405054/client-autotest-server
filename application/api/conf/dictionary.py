# _author: Coke
# _date: 2023/8/21 14:20

from application.api import api
from application import utils, db, models
from sqlalchemy import or_
from flask import request

import logging


@api.route('/conf/dictionary/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_dictionary_list():
    """
    获取字典列表
    :return:
    """

    body = request.get_json(silent=True)

    page = body.get('page')
    page = page if page else 0
    size = body.get('pageSize')
    size = size if size else 0
    keyword = body.get('keyword')
    keyword = keyword if keyword else ""

    query_list = [
        or_(models.Dictionary.name.like(f'%{keyword}%'), models.Dictionary.code.like(f'%{keyword}%'))
    ]

    data, total = utils.paginate(
        models.Dictionary,
        page,
        size,
        filter_list=query_list
    )

    return utils.rander(utils.OK, data=utils.paginate_structure(data, total, page, size))


@api.route('/conf/dictionary/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_dictionary_info():
    """
    新增/修改字典信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    dictionary_id = body.get('id')
    name = body.get('name')
    code = body.get('code')
    desc = body.get('desc')
    status = body.get('status')

    if not all([name, code, isinstance(status, bool)]):
        return utils.rander(utils.DATA_ERR)

    if dictionary_id:
        dictionary = models.Dictionary.query.filter_by(id=dictionary_id)

        if not dictionary.first():
            return utils.rander(utils.DATA_ERR, '此字典已不存在')

        update_dict = dict(
            name=name,
            code=code,
            desc=desc,
            status=status
        )

        try:
            dictionary.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    dictionary = models.Dictionary(name, code, desc, status)
    try:
        db.session.add(dictionary)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('conf/dictionary/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_dictionary_info():
    """
    删除字典信息
    :return:
    """

    return utils.delete(models.Dictionary, dict(id='id'))


@api.route('/conf/library/list', methods=['GET', 'POST'])
@utils.login_required
@utils.permissions_required
def get_library_list():
    """
    获取字典数据列表
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    code = body.get('code')
    page = body.get('page')
    page = page if page else 0
    size = body.get('pageSize')
    size = size if size else 0
    name = body.get('keyword')
    name = name if name else ""

    if not code:
        return utils.rander(utils.DATA_ERR)

    query_list = [models.Library.code == code, models.Library.name.like(f'%{name}%')]

    data, total = utils.paginate(models.Library, page, size, filter_list=query_list, order_by=models.Library.sort)

    return utils.rander(utils.OK, data=utils.paginate_structure(data, total, page, size))


@api.route('/conf/library/edit', methods=['POST', 'PUT'])
@utils.login_required
@utils.permissions_required
def edit_library_info():
    """
    新增/修改字典数据信息
    :return:
    """

    body = request.get_json()

    if not body:
        return utils.rander(utils.BODY_ERR)

    library_id = body.get('id')
    name = body.get('name')
    value_type = body.get('valueType')
    value = body.get('value')
    code = body.get('code')
    desc = body.get('desc')
    sort = body.get('sort')
    status = body.get('status')

    if not all([name, code, isinstance(status, bool), value, value_type, sort]):
        return utils.rander(utils.DATA_ERR)

    if library_id:
        library = models.Library.query.filter_by(id=library_id)

        if not library.first():
            return utils.rander(utils.DATA_ERR, '此字典数据已不存在')

        update_dict = dict(
            name=name,
            code=code,
            desc=desc,
            status=status,
            value_type=value_type,
            value=value,
            sort=sort
        )

        try:
            library.update(update_dict)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return utils.rander(utils.DATABASE_ERR)

        return utils.rander(utils.OK)

    library = models.Library(name, code, sort, value, value_type, desc, status)
    try:
        db.session.add(library)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return utils.rander(utils.DATABASE_ERR)

    return utils.rander(utils.OK)


@api.route('conf/library/delete', methods=['POST', 'DELETE'])
@utils.login_required
@utils.permissions_required
def delete_library_info():
    """
    删除字典数据信息
    :return:
    """

    return utils.delete(models.Library, dict(id='id'))
