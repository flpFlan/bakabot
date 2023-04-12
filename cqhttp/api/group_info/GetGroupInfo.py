"""获取群信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        group_id: int
        group_name: str
        group_memo: str
        group_create_time: int
        group_level: int
        member_count: int
        max_member_count: int

    data: Data


@register_to_api
class GetGroupInfo(ApiAction[Response]):
    """获取群信息"""

    action = "get_group_info"
    response: Response

    def __init__(
        self, group_id: int, no_cache: bool = False, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.no_cache = no_cache
        self.echo = echo
