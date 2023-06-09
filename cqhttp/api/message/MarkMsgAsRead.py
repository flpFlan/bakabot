"""标记消息已读"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class MarkMsgAsRead(ApiAction[ResponseBase]):
    """标记消息已读"""

    action = "mark_msg_as_read"

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.message_id = message_id
        self.echo = echo
