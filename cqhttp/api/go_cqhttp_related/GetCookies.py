"""获取 Cookies"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        cookies: str

    data: Data


@register_to_api
class GetCookies(ApiAction[Response]):
    """获取 Cookies"""

    action = "get_cookies"
    response: Response

    def __init__(self, domain: Optional[str] = None, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.domain = domain
        self.echo = echo
