# _author: Coke
# _date: 2023/8/11 11:26


from application import models, db


class Permissions:

    def __init__(self):
        self.projects()
        self.accounts()
        self.permissions()
        self.mock()
        self.devices()
        self.base()
        self.version()
        self._set()

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

    @staticmethod
    def devices():

        device = models.Menu('设备管理', 'Devices')
        db.session.add(device)
        db.session.commit()

        master = models.Menu('控制设备', 'DevicesMaster', device.id)
        db.session.add(master)
        db.session.commit()

        master_list = models.Menu('获取控制设备列表', '/devices/master/list', master.id)
        master_edit = models.Menu('编辑控制设备信息', '/devices/master/edit', master.id)
        master_delete = models.Menu('删除控制设备信息', '/devices/master/delete', master.id)
        master_status = models.Menu('修改控制设备当前状态', '/devices/master/status', master.id)
        master_info = models.Menu('获取控制设备信息', '/devices/master/info', master.id)
        master_socket = models.Menu('获取控制设备房间号', '/devices/master/socket', master.id)

        worker = models.Menu('执行设备', 'DevicesWorker', device.id)
        db.session.add(worker)
        db.session.commit()

        worker_list = models.Menu('获取工作设备列表', '/devices/worker/list', worker.id)
        worker_edit = models.Menu('编辑工作设备信息', '/devices/worker/edit', worker.id)
        worker_delete = models.Menu('删除工作设备信息', '/devices/worker/delete', worker.id)
        worker_status = models.Menu('修改工作机的设备状态', '/devices/worker/status', worker.id)
        worker_switch = models.Menu('开启/关闭执行机任务轮训', '/devices/worker/switch', worker.id)

        db.session.add_all([
            master_status, master_edit, master_delete, master_socket, master_info, master_list,
            worker_status, worker_switch, worker_delete, worker_edit, worker_list
        ])
        db.session.commit()

    @staticmethod
    def base():
        base = models.Menu('基础配置', 'Base')
        db.session.add(base)
        db.session.commit()

        element = models.Menu('页面元素', 'BaseElement', base.id)
        db.session.add(element)
        db.session.commit()

        element_list = models.Menu('获取页面元素列表', '/conf/element/list', element.id)
        element_edit = models.Menu('编辑页面元素信息', '/conf/element/edit', element.id)
        element_delete = models.Menu('删除页面元素信息', '/conf/element/delete', element.id)

        dictionary = models.Menu('字典管理', 'BaseDict', base.id)
        db.session.add(dictionary)
        db.session.commit()

        dictionary_list = models.Menu('获取字典列表', '/conf/dictionary/list', dictionary.id)
        dictionary_edit = models.Menu('编辑字典信息', '/conf/dictionary/edit', dictionary.id)
        dictionary_delete = models.Menu('删除字典信息', '/conf/dictionary/delete', dictionary.id)
        library_list = models.Menu('获取字典数据列表', '/conf/library/list', dictionary.id)
        library_edit = models.Menu('编辑字典数据信息', '/conf/library/edit', dictionary.id)
        library_delete = models.Menu('删除字典数据信息', '/conf/library/delete', dictionary.id)

        db.session.add_all([element_edit, element_list, element_delete, dictionary_delete, dictionary_edit,
                            dictionary_list, library_list, library_delete, library_edit])
        db.session.commit()

    @staticmethod
    def version():
        base = models.Menu('版本管理', 'Version')
        db.session.add(base)
        db.session.commit()

        version = models.Menu('版本管理', 'VersionIndex', base.id)
        db.session.add(version)
        db.session.commit()

        version_list = models.Menu('获取版本列表', '/business/version/list', version.id)
        version_edit = models.Menu('编辑版本信息', '/business/version/edit', version.id)
        version_delete = models.Menu('删除版本信息', '/business/version/delete', version.id)

        db.session.add_all([version_edit, version_list, version_delete])
        db.session.commit()

    @staticmethod
    def _set():
        base = models.Menu('测试集合', 'Set')
        db.session.add(base)
        db.session.commit()

        set_index = models.Menu('测试集合', 'SetIndex', base.id)
        db.session.add(set_index)
        db.session.commit()

        set_list = models.Menu('获取测试集合列表', '/business/set/list', set_index.id)
        set_edit = models.Menu('编辑测试集合信息', '/business/set/edit', set_index.id)
        set_delete = models.Menu('删除测试集合信息', '/business/set/delete', set_index.id)

        db.session.add_all([set_edit, set_list, set_delete])
        db.session.commit()
