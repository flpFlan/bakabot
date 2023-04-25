"""获取陌生人信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        user_id: int
        nickname: str
        sex: str
        age: int
        qid: str
        level: int
        login_days: int

    data: Data


@register_to_api
class GetStrangerInfo(ApiAction[Response]):
    """获取陌生人信息"""

    action = "get_stranger_info"
    response: Response

    def __init__(
        self, user_id: int, no_cache: bool = False, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.user_id = user_id
        self.echo = echo
