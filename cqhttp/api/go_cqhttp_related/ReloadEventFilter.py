"""重载事件过滤器"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class ReloadEventFilter(ApiAction[ResponseBase]):
    """重载事件过滤器"""

    action = "reload_event_filter"

    def __init__(self, file: str, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.file = file
        self.echo = echo
