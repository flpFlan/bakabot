"""获取精华消息列表"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Element:
        sender_id: int
        sender_nick: str
        sender_time: int
        operator_id: int
        operator_nick: str
        operator_time: int
        message_id: int

    data: list[Element]


@register_to_api
class GetEssenceMsgList(ApiAction[Response]):
    """获取精华消息列表"""

    action = "get_essence_msg_list"
    response: Response

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.echo = echo
