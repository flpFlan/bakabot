from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class NoticeInfo:
        class Message:
            text: str
            images: list[str]

        sender_id: int
        publish_time: int
        message: Message

    data: list[NoticeInfo]


@register_to_api
class GetGroupNotice(ApiAction[Response]):
    """获取群公告"""

    action = "_get_group_notice"
    response = Response()

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        self.group_id = group_id
        self.echo = echo
