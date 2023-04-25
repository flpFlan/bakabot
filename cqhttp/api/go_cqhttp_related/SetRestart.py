"""重启 Go-CqHttp"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SetRestart(ApiAction[ResponseBase]):
    """重启 Go-CqHttp"""

    action = "set_restart"

    def __init__(self, delay: int = 0, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.delay = delay
        self.echo = echo
