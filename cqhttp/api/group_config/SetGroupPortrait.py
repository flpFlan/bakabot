from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupPortrait(ApiAction):
    """设置群头像"""

    action = "set_group_portrait"

    def __init__(
        self, group_id: int, file: str, cache: int = 1, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.file = file
        self.cache = cache
        self.echo = echo
