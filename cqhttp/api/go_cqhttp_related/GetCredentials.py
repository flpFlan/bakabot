"""获取 QQ 相关接口凭证"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        cookies: str
        csrf_token: int

    data: Data


@register_to_api
class GetCredentials(ApiAction[Response]):
    """获取 QQ 相关接口凭证"""

    action = "get_credentials"
    response: Response

    def __init__(self, domain: Optional[str] = None, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.domain = domain
        self.echo = echo
