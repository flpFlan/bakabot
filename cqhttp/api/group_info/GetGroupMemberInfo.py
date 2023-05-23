"""获取群成员信息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    group_id: int
    user_id: int
    nickname: str
    card: str
    sex: str
    age: int
    area: str
    join_time: int
    last_sent_time: int
    level: str
    role: str
    unfriendly: bool
    title: str
    title_expire_time: int
    card_changeable: bool
    shut_up_timestamp: int
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupMemberInfo(ApiAction[Response]):
    """获取群成员信息"""

    action:str = field(init=False,default="get_group_member_info")
    group_id: int
    user_id: int
    no_cache: bool = False
