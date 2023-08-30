# _author: Coke
# _date: 2022/8/15 14:01

from .messageEmail import MessageEmail
from .robot import MessageRobot
from .element import Element
from .event import Event
from .dictionary import Dictionary, Library
from .magic import MagicMenu
from .dynamic import DynamicElement

__all__ = [
    'MessageEmail',
    'MessageRobot',
    'Element',
    'Event',
    'Dictionary',
    'Library',
    'DynamicElement',
    'MagicMenu'
]
