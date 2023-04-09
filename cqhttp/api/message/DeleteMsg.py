from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteMsg(ApiAction):
    """撤回消息"""

    action = "delete_msg"

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        self.message_id = message_id
        self.echo = echo
