from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        level: int

    data: Data


@register_to_api
class CheckUrlSafely(ApiAction[Response]):
    """检查链接安全性"""

    action = "check_url_safely"
    response = Response()

    def __init__(self, url: str, *, echo: Optional[str] = None):
        self.url = url
        self.echo = echo
