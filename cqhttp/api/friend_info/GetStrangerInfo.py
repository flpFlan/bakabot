"""获取陌生人信息"""
from dataclasses import dataclass, field
from typing import  TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    user_id: int
    nickname: str
    sex: str
    age: int
    qid: str
    level: int
    login_days: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetStrangerInfo(ApiAction[Response]):
    """获取陌生人信息"""

    action:str = field(init=False,default="get_stranger_info")
    user_id: int
    no_cache: bool = False
