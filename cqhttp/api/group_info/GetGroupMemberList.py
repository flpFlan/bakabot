"""获取群成员列表"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.api.group_info.GetGroupMemberInfo import Response as Res


class Response(ResponseBase):
    class Info:
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

    data: list[Info]


@register_to_api
class GetGroupMemberList(ApiAction[Response]):
    """获取群成员列表"""

    action = "get_group_member_list"
    response: Response

    def __init__(
        self, group_id: int, no_cache: bool = False, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.no_cache = no_cache
        self.echo = echo
