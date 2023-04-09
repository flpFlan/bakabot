from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        from cqhttp.events.message import GroupMessage

        messages: list[GroupMessage]

    data: Data


@register_to_api
class GetGroupMsgHistory(ApiAction[Response]):
    """获取群消息历史记录"""

    action = "get_group_msg_history"
    response = Response()

    def __init__(
        self,
        group_id: int,
        message_seq: Optional[int] = None,
        *,
        echo: Optional[str] = None
    ):
        self.message_seq = message_seq
        self.group_id = group_id
        self.echo = echo
