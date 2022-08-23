# _author: Coke
# _date: 2022/8/23 17:29

from .user import User, models, db


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
            '这是一个基于 Appium 框架开发的 UI 自动化程序 ...',
            'https://wpimg.wallstcn.com/9e2a5d0a-bd5b-457f-ac8e-86554616c87b.jpg',
            'selenium',
            'admin',
            self.user.id
        )

        db.session.add(self.wechat)
        db.session.add(self.baidu)
        db.session.commit()

        self.set_element()

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
