from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class CleanCache(ApiAction):
    """清理缓存"""

    action = "clean_cache"

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
