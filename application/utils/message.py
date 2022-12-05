# _author: Coke
# _date: 2022/12/5 13:35

from application import socketio


def common(_type='info', duration=2):
    """
    处理类型和持续时间
    :param _type:
    :param duration:
    :return:
    """
    type_list = [
        'error',
        'info',
        'success',
        'warning'
    ]
    _type = _type if _type in type_list else 'info'

    duration = duration * 1000 if duration < 60 else 2 * 1000

    return _type, duration


def message(_message, _type='info', duration=2, sid=None):
    """
    发送一个普通长链消息
    :param _message: 消息
    :param _type: 类型
    :param duration: 持续时长
    :param sid: 指定的房间信息
    :return:
    """
    if not _message:
        return

    _type, duration = common(_type, duration)

    _message = dict(
        message=_message,
        type=_type,
        duration=duration
    )

    socketio.emit('message', _message, room=sid)


def notify(title, _message, _type='info', duration=2, sid=None, **kwargs):
    """
    发送一个通知类消息
    :param title: 消息标题
    :param _message: 消息内容
    :param _type: 消息类型
    :param duration: 持续时间
    :param sid: 房间id
    :param kwargs:
    position: 弹窗出现的位置
    html: 是否为 html 片段
    offset: 是否偏移， 要偏移的像素
    showClose: 是否可以关闭, 默认为 True 可以关闭
    :return:
    """
    position_list = [
        'top-right',
        'top-left',
        'bottom-left',
        'bottom-right'
    ]
    position = kwargs.pop('position', 'top-right')
    position = position if position in position_list else 'top-right'
    html = kwargs.pop('html', False)
    offset = kwargs.pop('offset', 0)
    show_close = kwargs.pop('showClose', True)

    if not _message or not title:
        return

    _type, duration = common(_type, duration)

    _message = dict(
        message=_message,
        title=title,
        type=_type,
        duration=duration,
        position=position,
        dangerouslyUseHTMLString=html,
        offset=offset,
        showClose=show_close
    )

    socketio.emit('notify', _message, room=sid)
