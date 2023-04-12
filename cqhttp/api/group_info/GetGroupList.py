"""获取群列表"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.api.group_info.GetGroupInfo import Response as Res


class Response(ResponseBase):
    data: list[Res]


@register_to_api
class GetGroupList(ApiAction[Response]):
    """获取群列表"""

    action = "get_group_list"
    response: Response

    def __init__(self, no_cache: bool = False, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.no_cache = no_cache
        self.echo = echo
