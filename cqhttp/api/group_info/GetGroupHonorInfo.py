"""获取群荣誉信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class CurrentTalkative:
            user_id: int
            nickname: str
            avatar: str
            day_count: int

        class MemberInfo:
            user_id: int
            nickname: str
            avatar: str
            description: str

        group_id: int
        current_talkative: CurrentTalkative | None
        talkative_list: list[MemberInfo] | None
        performer_list: list[MemberInfo] | None
        legend_list: list[MemberInfo] | None
        strong_newbie_list: list[MemberInfo] | None
        emotion_list: list[MemberInfo] | None

    data: Data


@register_to_api
class GetGroupHonorInfo(ApiAction[Response]):
    """获取群荣誉信息"""

    action = "get_group_honor_info"
    response = Response()

    def __init__(self, group_id: int, type: str = "all", *, echo: Optional[str] = None):
        self.group_id = group_id
        self.type = type
        self.echo = echo
