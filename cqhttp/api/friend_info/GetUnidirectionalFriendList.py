from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        user_id: int
        nickname: str
        source: str


@register_to_api
class GetUnidirectionalFriendList(ApiAction[Response]):
    """获取单向好友列表"""

    action = "get_unidirectional_friend_list"
    response = Response()

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
