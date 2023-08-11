# _author: Coke
# _date: 2023/2/22 11:11

from application import utils, SOCKET_HOST
from application.api import api, swagger


@api.route('/conf/socket/domain', methods=['GET', 'POST'])
@utils.login_required
@swagger('socketDomain.yaml')
def get_socket_domain():
    """ 获取 socket 域名信息 """

    return utils.rander(utils.OK, data=dict(domain=f'{SOCKET_HOST}'))
