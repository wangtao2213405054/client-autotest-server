# _author: Coke
# _date: 2022/8/10 14:55

from datetime import datetime
from sqlalchemy import Column
from application import db
from abc import abstractmethod


class BaseModel:
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

    @property
    @abstractmethod
    def result(self): ...  # 获取模型 dict

    @abstractmethod
    def __init__(self, **kwargs): ...
