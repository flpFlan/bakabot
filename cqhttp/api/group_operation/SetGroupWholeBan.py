from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupWholeBan(ApiAction):
    """群全员禁言"""

    action = "set_group_whole_ban"

    def __init__(
        self, group_id: int, enable: bool = True, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.enable = enable
        self.echo = echo
