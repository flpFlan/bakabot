"""获取群成员信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
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

    data: Data


@register_to_api
class GetGroupMemberInfo(ApiAction[Response]):
    """获取群成员信息"""

    action = "get_group_member_info"
    response: Response

    def __init__(
        self,
        group_id: int,
        user_id: int,
        no_cache: bool = False,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.user_id = user_id
        self.no_cache = no_cache
        self.echo = echo
