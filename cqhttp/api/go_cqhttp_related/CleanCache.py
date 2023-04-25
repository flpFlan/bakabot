"""清理缓存"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class CleanCache(ApiAction[ResponseBase]):
    """清理缓存"""

    action = "clean_cache"

    def __init__(self, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.echo = echo
