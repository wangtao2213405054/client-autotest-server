# _author: Coke
# _date: 2022/8/23 17:29

from .user import User, models, db

import time


class Project(User):

    def __init__(self):
        super().__init__()

        self.wechat = models.Project(
            '微信',
            '这是一个基于 Appium 框架开发的 UI 自动化程序 ...',
            'https://wpimg.wallstcn.com/57ed425a-c71e-4201-9428-68760c0537c4.jpg',
            mold='appium',
            create_user='admin',
            create_id=self.user.id
        )

        self.baidu = models.Project(
            '百度',
            '这是一个基于 Selenium 框架开发的 UI 自动化程序 ...',
            'https://wpimg.wallstcn.com/9e2a5d0a-bd5b-457f-ac8e-86554616c87b.jpg',
            'selenium',
            'admin',
            self.user.id
        )

        db.session.add(self.wechat)
        db.session.add(self.baidu)
        db.session.commit()

        self.set_element()

        self.set_event()
        # 设置用例表从百万开始
        db.session.execute(f'ALTER TABLE {models.Case.__tablename__} AUTO_INCREMENT = 1000000')

    @classmethod
    def set_element(cls):
        mold = ['appium', 'selenium']
        ios_predicate = models.Element(
            'IOS_PREDICATE',
            '-ios predicate string',
            'iOS 设备原生支持的 Predicate 定位方式',
            mold[0: 1]
        )
        ios_uiautomation = models.Element(
            'IOS_UIAUTOMATION',
            '-ios uiautomation',
            'iOS 的谓词查找，类似于 XPATH 的谓词定位',
            mold[0: 1]
        )
        ios_class_chain = models.Element(
            'IOS_CLASS_CHAIN',
            '-ios class chain',
            'iOS 10以上版本可使用此类型链',
            mold[0: 1]
        )
        android_uiautomator = models.Element(
            'ANDROID_UIAUTOMATOR',
            '-android uiautomator',
            '仅支持 UiAutomator2 引擎，它使用 UI Automator 来定位元素',
            mold[0: 1]
        )
        android_view_tag = models.Element(
            'ANDROID_VIEWTAG',
            '-android viewtag',
            '它使用View Tag来定位元素',
            mold[0: 1]
        )
        android_data_matcher = models.Element(
            'ANDROID_DATA_MATCHER',
            '-android datamatcher',
            '它使用用于查找数据对象的匹配器来定位元素',
            mold[0: 1]
        )
        android_view_matcher = models.Element(
            'ANDROID_VIEW_MATCHER',
            '-android viewmatcher',
            '它使用用于查找数据视图的匹配器来定位元素',
            mold[0: 1]
        )

        _id = models.Element(
            'ID',
            'id',
            '通过元素的 id 属性来定位元素',
            mold
        )
        xpath = models.Element(
            'XPATH',
            'xpath',
            '通过元素的 路径 来定位元素, 效率较慢维护成本较高不推荐使用',
            mold
        )
        link_text = models.Element(
            'LINK_TEXT',
            'link text',
            '用于定位超链接文本',
            mold
        )
        partial_link_text = models.Element(
            'PARTIAL_LINK_TEXT',
            'partial link text',
            '模糊匹配并定位超链接文本',
            mold
        )
        name = models.Element(
            'NAME',
            'name',
            '通过元素的 name 属性来定位元素',
            mold
        )
        tag_name = models.Element(
            'TAG_NAME',
            'tag name',
            '通过标签进行定位',
            mold
        )
        class_name = models.Element(
            'CLASS_NAME',
            'class name',
            '通过元素的 class name 属性来定位元素',
            mold
        )
        css_selector = models.Element(
            'CSS_SELECTOR',
            'css selector',
            'CSS 定位方式',
            mold
        )

        db.session.add_all([
            ios_predicate,
            ios_uiautomation,
            ios_class_chain,
            android_uiautomator,
            android_view_tag,
            android_data_matcher,
            android_view_matcher,
            css_selector,
            partial_link_text,
            link_text,
            tag_name,
            class_name,
            name,
            xpath,
            _id
        ])
        db.session.commit()

    @staticmethod
    def get_map(data_type, default, param, placeholder, select_model, title, event_type, source=None):
        mapping = dict(
            collapse='',
            dataType=data_type,
            default=default,
            key=time.time(),
            param=param,
            placeholder=placeholder,
            selectModel=select_model,
            source=source if source else [],
            title=title,
            type=event_type
        )
        time.sleep(0.01)
        return mapping

    @staticmethod
    def get_source(label, param, data_type):
        source = dict(
            key=time.time(),
            label=label,
            param=param,
            dataType=data_type
        )
        time.sleep(0.01)
        return source

    def set_event(self):
        event_list = [
            models.Event(
                '点击事件',
                'find_elements_click',
                'all',
                self.wechat.id,
                '点击元素',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            ),
            models.Event(
                '清空文本',
                'find_elements_clear',
                'all',
                self.wechat.id,
                '清除文本框中已经输入的数据',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            ),
            models.Event(
                '输入文本',
                'find_elements_send_keys',
                'all',
                self.wechat.id,
                '在文本输入框中输入数据',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('String', None, 'content', '请输入要写入的内容', None, '输入内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            ),
            models.Event(
                '隐式等待',
                'wait_elements_appear',
                'all',
                self.wechat.id,
                '等待某一个元素出现',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input'),
                    self.get_map('Integer', 5, 'wait_time', '请输入最大等待时间', None, '等待时间', 'input'),
                    self.get_map('Float', 0.5, 'interval', '请输入检测间隔', None, '检测间隔', 'input')
                ],
                True
            ),
            models.Event(
                '置于后台',
                'background',
                'appium',
                self.wechat.id,
                '将应用置于后台',
                [
                    self.get_map('Integer', None, 'timer', '请输入应用置于后台的时间', None, '隐藏时间', 'input'),
                ]
            ),
            models.Event(
                '设置位置',
                'set_location',
                'appium',
                self.wechat.id,
                '设置当前设备所处于的位置',
                [
                    self.get_map('String', None, 'longitude', '请输入要设置的经度', None, '设置经度', 'input'),
                    self.get_map('String', None, 'latitude', '请输入要设置的纬度', None, '设置纬度', 'input'),
                    self.get_map('String', None, 'altitude', '请输入要设置的高度', None, '设置高度', 'input')
                ]
            ),
            models.Event(
                '屏幕滑动',
                'find_window_swipe',
                'appium',
                self.wechat.id,
                '在当前设备屏幕上进行滑动',
                [
                    self.get_map('String', None, 'handle', '请选择要滑动的方向', 'Custom', '滑动方向', 'select',
                                 [
                                     self.get_source('纵向滑动', 'vertical', 'String'),
                                     self.get_source('横向滑动', 'horizontal', 'String')
                                 ]),
                    self.get_map('Float', None, 'start', '请输入开始滑动位置的比例', None, '开始位置', 'input'),
                    self.get_map('Float', None, 'end', '请输入滑动结束位置的比例', None, '结束位置', 'input'),
                    self.get_map('Float', None, 'duration', '请输入滑动开始到结束之间的时长', None, '滑动时长', 'input'),
                ]
            ),
            models.Event(
                '元素滑动',
                'find_element_swipe',
                'appium',
                self.wechat.id,
                '寻找到指定的元素后在元素中进行按压滑动',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input'),
                    self.get_map('String', None, 'handle', '请选择要滑动的方向', 'Custom', '滑动方向', 'select',
                                 [
                                     self.get_source('纵向滑动', 'vertical', 'String'),
                                     self.get_source('横向滑动', 'horizontal', 'String')
                                 ]),
                    self.get_map('Float', None, 'start', '请输入开始滑动位置的比例', None, '开始位置', 'input'),
                    self.get_map('Float', None, 'end', '请输入滑动结束位置的比例', None, '结束位置', 'input'),
                    self.get_map('Float', None, 'duration', '请输入滑动开始到结束之间的时长', None, '滑动时长', 'input'),
                ]
            ),
            models.Event(
                '退出程序',
                'quit',
                'selenium',
                self.baidu.id,
                '关闭当前浏览器的进程',
                []
            ),
            models.Event(
                '关闭窗口',
                'close',
                'selenium',
                self.baidu.id,
                '关闭当前浏览器页面的窗口',
                []
            ),
            models.Event(
                '存储信息',
                'save_cookies',
                'selenium',
                self.baidu.id,
                '获取当前浏览器的 cookies 并存储在本地变量中',
                []
            ),
            models.Event(
                '写入信息',
                'write_cookies',
                'selenium',
                self.baidu.id,
                '将本地存储的 cookies 写入浏览器, 和存储信息搭配使用',
                []
            ),
            models.Event(
                '删除信息',
                'delete_cookies',
                'selenium',
                self.baidu.id,
                '将本地存储的 cookies 删除',
                []
            ),
            models.Event(
                '刷新页面',
                'refresh',
                'selenium',
                self.baidu.id,
                '刷新当前浏览器页面',
                []
            ),
            models.Event(
                '返回上级',
                'back',
                'selenium',
                self.baidu.id,
                '返回到上一级页面',
                []
            ),
            models.Event(
                '前进下级',
                'selenium_forward_browser',
                'selenium',
                self.baidu.id,
                '前进到下一级页面',
                []
            ),
            models.Event(
                '切换窗口',
                'switch_window',
                'selenium',
                self.baidu.id,
                '当存在多个窗口时，需要使用此方法进行切换',
                [
                    self.get_map('Integer', None, 'window', '请输入要切换的窗口', None, '窗口信息', 'input'),
                ]
            ),
            models.Event(
                '右击事件',
                'context_click',
                'selenium',
                self.baidu.id,
                '右击元素',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            ),
            models.Event(
                '双击事件',
                'double_click',
                'selenium',
                self.baidu.id,
                '双击元素',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            ),
            models.Event(
                '悬停事件',
                'move_element',
                'selenium',
                self.baidu.id,
                '将鼠标悬停在元素上',
                [
                    self.get_map('String', 'id', 'by', '请选择元素类型', 'Element', '元素类型', 'select'),
                    self.get_map('String', None, 'value', '请输入元素元素内容', None, '元素内容', 'input'),
                    self.get_map('Integer', 0, 'index', '请选择元素位置', 'ElementIndex', '元素位置', 'select'),
                    self.get_map('String', None, 'name', '请输入元素名称', None, '元素名称', 'input')
                ]
            )
        ]
        db.session.add_all(event_list)
        db.session.commit()
