"""获取 CSRF Token"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        token: int

    data: Data


@register_to_api
class GetCsrfToken(ApiAction[Response]):
    """获取 CSRF Token"""

    action = "get_csrf_token"
    response: Response

    def __init__(self, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.echo = echo
