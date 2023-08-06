# _author: Coke
# _date: 2022/12/5 12:00

from application.api import api
from application import utils


@api.route('/message/notification/new', methods=['GET', 'POST'])
# @utils.login_required
# @utils.permissions_required
def send_notification_info():
    """ 发送通知消息 """

    utils.message('这是一个测试的消息')
    utils.notify(
        '测试',
        '嗯，这就是一个测试消息哇',
    )
    return utils.rander(utils.OK)
