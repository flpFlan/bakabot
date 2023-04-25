"""获取群系统消息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class InvitedRequest:
            request_id: int
            invitor_uin: int
            invitor_nick: str
            group_id: int
            group_name: str
            checked: bool
            actor: int

        class JoinRequest:
            request_id: int
            requester_uin: int
            requester_nick: str
            message: str
            group_id: int
            group_name: str
            checked: bool
            actor: int

        invited_requests: list[InvitedRequest]
        join_requests: list[JoinRequest]

    data: Data


@register_to_api
class GetGroupSystemMsg(ApiAction[Response]):
    """获取群系统消息"""

    action = "get_group_system_msg"
    response: Response

    def __init__(self, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.echo = echo
