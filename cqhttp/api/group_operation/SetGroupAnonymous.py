from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupAnonymous(ApiAction):
    """群设置匿名"""

    action = "set_group_anonymous"

    def __init__(
        self, group_id: int, enable: bool = True, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.enable = enable
        self.echo = echo
