# _author: Coke
# _date: 2022/8/15 14:23

from tests.config import *
import unittest
import requests


class Message(unittest.TestCase):

    url = HOST + URI

    def setUp(self) -> None: ...
    def tearDown(self) -> None: ...

    def test_get_email_info(self):
        body = dict(
            projectId=1
        )
        data = requests.request('POST', self.url + '/message/email/info', json=body)
        self.assertEqual(data.status_code, 200)
        print(data.json())

    def test_edit_email(self):
        body = dict(
            projectId=1,
            host='smtp.qq.com',
            title='测试邮件',
            sender='Coke',
            password='123456',
            receivers=['coke@qq.com'],
            state=False
        )
        data = requests.request('POST', self.url + '/message/email/edit', json=body)
        print(data.status_code)
