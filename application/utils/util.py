# _author: Coke
# _date: 2022/12/30 11:56

import pypinyin


def pinyin(_str):
    """ 将汉字转换为拼音 """

    _pinyin = ''
    for item in pypinyin.pinyin(_str, style=pypinyin.NORMAL):
        _pinyin += ''.join(item).capitalize()

    return _pinyin
