"""获取群荣誉信息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class CurrentTalkative(TypedDict):
    user_id: int
    nickname: str
    avatar: str
    day_count: int

class MemberInfo(TypedDict):
    user_id: int
    nickname: str
    avatar: str
    description: str

class Data(TypedDict):
    group_id: int
    current_talkative: CurrentTalkative | None
    talkative_list: list[MemberInfo] | None
    performer_list: list[MemberInfo] | None
    legend_list: list[MemberInfo] | None
    strong_newbie_list: list[MemberInfo] | None
    emotion_list: list[MemberInfo] | None

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupHonorInfo(ApiAction[Response]):
    """获取群荣誉信息"""

    action:str = field(init=False,default="get_group_honor_info")
    group_id: int
    type: str = "all"
