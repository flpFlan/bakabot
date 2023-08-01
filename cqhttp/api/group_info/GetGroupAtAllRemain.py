"""获取群 @全体成员 剩余次数"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    can_at_all: bool
    remain_at_all_count_for_group: int
    remain_at_all_count_for_uin: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupAtAllRemain(ApiAction[Response]):
    """获取群 @全体成员 剩余次数"""

    action:str = field(init=False,default="get_group_at_all_remain")
    group_id: int
