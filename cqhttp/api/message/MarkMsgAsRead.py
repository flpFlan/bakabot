from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class MarkMsgAsRead(ApiAction):
    """标记消息已读"""

    action = "mark_msg_as_read"

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        self.message_id = message_id
        self.echo = echo
