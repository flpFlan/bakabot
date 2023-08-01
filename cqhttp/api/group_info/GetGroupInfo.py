"""获取群信息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    group_id: int
    group_name: str
    group_memo: str
    group_create_time: int
    group_level: int
    member_count: int
    max_member_count: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupInfo(ApiAction[Response]):
    """获取群信息"""

    action:str = field(init=False,default="get_group_info")
    group_id: int
    no_cache: bool = False
