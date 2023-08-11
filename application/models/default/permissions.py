# _author: Coke
# _date: 2023/8/11 11:26


from application import models, db


class Permissions:

    def __init__(self):
        self.projects()
        self.accounts()
        self.permissions()
        self.mock()

    @staticmethod
    def projects():
        project = models.Menu('项目列表', 'Project')
        db.session.add(project)
        db.session.commit()

        project_list = models.Menu('获取项目列表', '/business/project/list', project.id)
        project_edit = models.Menu('编辑项目信息', '/business/project/edit', project.id)
        project_delete = models.Menu('删除项目信息', '/business/project/delete', project.id)
        project_info = models.Menu('获取项目信息', '/business/project/info', project.id)

        db.session.add_all([project_list, project_delete, project_edit, project_info])
        db.session.commit()

    @staticmethod
    def accounts():
        account = models.Menu('用户列表', 'Account')
        db.session.add(account)
        db.session.commit()

        account_child = models.Menu('用户管理', 'AccountTeam', account.id)

        db.session.add(account_child)
        db.session.commit()

        classification_list = models.Menu('获取关系分类列表', '/account/classification/list', account_child.id)
        classification_edit = models.Menu('编辑关系分类', '/account/classification/edit', account_child.id)
        classification_delete = models.Menu('删除关系分类', '/account/classification/delete', account_child.id)

        user_list = models.Menu('获取用户列表', '/account/user/list', account_child.id)
        user_edit = models.Menu('编辑用户信息', '/account/user/edit', account_child.id)
        user_delete = models.Menu('删除用户信息', '/account/user/delete', account_child.id)
        user_query = models.Menu('通过ID列表查询用户', '/account/user/ids', account_child.id)

        db.session.add_all([classification_delete, classification_edit, classification_list, user_delete, user_edit,
                            user_query, user_list])
        db.session.commit()

    @staticmethod
    def permissions():
        permission = models.Menu('权限管理', 'Permission')
        db.session.add(permission)
        db.session.commit()

        role = models.Menu('角色管理', 'PermissionRole', permission.id)

        db.session.add(role)
        db.session.commit()

        role_list = models.Menu('获取角色列表', '/permissions/role/list', role.id)
        role_edit = models.Menu('编辑角色信息', '/permissions/role/edit', role.id)
        role_delete = models.Menu('删除角色信息', '/permissions/role/delete', role.id)

        menu = models.Menu('菜单管理', 'PermissionMenu', permission.id)

        db.session.add(menu)
        db.session.commit()

        menu_list = models.Menu('获取菜单列表', '/permissions/menu/list', menu.id)
        menu_edit = models.Menu('编辑菜单信息', '/permissions/menu/edit', menu.id)
        menu_delete = models.Menu('删除菜单信息', '/permissions/menu/delete', menu.id)

        db.session.add_all([role_delete, role_edit, role_list, menu_delete, menu_edit, menu_list])
        db.session.commit()

    @staticmethod
    def mock():
        mocks = models.Menu('模拟配置', 'Mock')
        db.session.add(mocks)
        db.session.commit()

        domain = models.Menu('域名配置', 'MockDomain', mocks.id)

        db.session.add(domain)
        db.session.commit()

        domain_list = models.Menu('获取域名列表', '/mock/domain/list', domain.id)
        domain_edit = models.Menu('编辑域名信息', '/mock/domain/edit', domain.id)
        domain_delete = models.Menu('删除域名信息', '/mock/domain/delete', domain.id)

        api = models.Menu('接口配置', 'MockApi', mocks.id)

        db.session.add(api)
        db.session.commit()

        api_list = models.Menu('获取接口列表', '/mock/api/list', api.id)
        api_edit = models.Menu('编辑接口信息', '/mock/api/edit', api.id)
        api_delete = models.Menu('删除接口信息', '/mock/api/delete', api.id)

        db.session.add_all([domain_delete, domain_edit, domain_list, api_delete, api_edit, api_list])
        db.session.commit()
