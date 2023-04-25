"""获取群 @全体成员 剩余次数"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        can_at_all: bool
        remain_at_all_count_for_group: int
        remain_at_all_count_for_uin: int

    data: Data


@register_to_api
class GetGroupAtAllRemain(ApiAction[Response]):
    """获取群 @全体成员 剩余次数"""

    action = "get_group_at_all_remain"
    response: Response

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.echo = echo
