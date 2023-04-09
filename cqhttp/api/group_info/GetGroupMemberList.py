from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.api.group_info.GetGroupMemberInfo import Response as Res


class Response(ResponseBase):
    data: list[Res]


@register_to_api
class GetGroupMemberList(ApiAction[Response]):
    """获取群成员列表"""

    action = "get_group_member_list"
    response = Response()

    def __init__(
        self, group_id: int, no_cache: bool = False, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.no_cache = no_cache
        self.echo = echo
