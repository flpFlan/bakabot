"""获取群成员列表"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Info(TypedDict):
    age: int
    card: str
    card_changeable: bool
    group_id: int
    join_time: int
    last_sent_time: int
    level: str
    nickname: str
    role: str
    sex: str
    shut_up_timestamp: int
    title: str
    title_expire_time: int
    unfriendly: bool
    user_id: int

class Response(ResponseBase):
    data: list[Info]


@ApiAction.register
@dataclass
class GetGroupMemberList(ApiAction[Response]):
    """获取群成员列表"""

    action:str = field(init=False,default="get_group_member_list")
    group_id: int
    no_cache: bool = False
