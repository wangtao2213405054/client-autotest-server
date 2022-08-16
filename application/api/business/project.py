# _author: Coke
# _date: 2022/5/3 12:51

from flask import request, g
from application.utils import rander, paginate_structure, login_required, permissions_required
from application.api import api
from application import models, db

import logging
import random


@api.route('/business/project/edit', methods=['POST', 'PUT'])
@login_required
@permissions_required
def edit_project_info():
    """ 新增/编辑项目信息 """

    body = request.get_json()

    if not body:
        rander('BODY_ERR')

    project_id = body.get('id')
    name = body.get('name')
    describe = body.get('describe')
    avatar = body.get('avatar')
    mold = body.get('mold')
    avatar_list = [
        'https://wpimg.wallstcn.com/57ed425a-c71e-4201-9428-68760c0537c4.jpg',
        'https://wpimg.wallstcn.com/9e2a5d0a-bd5b-457f-ac8e-86554616c87b.jpg',
        'https://wpimg.wallstcn.com/fb57f689-e1ab-443c-af12-8d4066e202e2.jpg'
    ]

    if not all([name, describe]):
        rander('DATA_ERR')

    if not avatar:
        avatar = random.choice(avatar_list)

    if project_id:
        project_info = models.Project.query.filter_by(id=project_id)

        if not project_info.first():
            return rander('DATA_ERR', '此项目已不存在')

        update_dict = {
            'name': name,
            'describe': describe,
            'avatar': avatar,
            'create_user': g.user_name,
            'create_id': g.user_id,
            'mold': mold
        }
        try:
            project_info.update(update_dict)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return rander('DATABASE_ERR')

        return rander('OK')

    project_info = models.Project(name, describe, avatar, mold, g.user_name, g.user_id)
    try:
        db.session.add(project_info)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return rander('DATABASE_ERR')

    return rander('OK')


@api.route('/business/project/list', methods=['GET', 'POST'])
@login_required
@permissions_required
def get_project_list():
    """ 获取项目列表 """

    body = request.get_json()

    if not body:
        return rander('BODY_ERR')

    name = body.get('name')
    page = body.get('page')
    page_size = body.get('pageSize')

    query_list = [
        models.Project.name.like(f'%{name if name else ""}%')
    ]

    project = models.Project.query.filter(*query_list).order_by(models.Project.id.desc())
    project_list = project.paginate(page, page_size, False).items
    project_count = project.count()

    project_dict_list = []
    for items in project_list:
        item = items.to_dict()
        item['label'] = f'{items.create_user} 更新与 {items.update_time}'
        project_dict_list.append(item)

    return rander('OK', data=paginate_structure(project_dict_list, project_count, page, page_size))


@api.route('/business/project/delete', methods=['POST', 'DELETE'])
@login_required
@permissions_required
def delete_project_info():
    """ 删除项目信息 """

    body = request.get_json()

    if not body:
        return rander('BODY_ERR')

    project_id = body.get('id')

    project = models.Project.query.filter_by(id=project_id)

    if not project.first():
        return rander('DATA_ERR', '此项目已不存在')

    try:
        project.delete()
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return rander('DATABASE_ERR')

    return rander('OK')
