"""获取群系统消息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class InvitedRequest(TypedDict):
    request_id: int
    invitor_uin: int
    invitor_nick: str
    group_id: int
    group_name: str
    checked: bool
    actor: int

class JoinRequest(TypedDict):
    request_id: int
    requester_uin: int
    requester_nick: str
    message: str
    group_id: int
    group_name: str
    checked: bool
    actor: int
    
class Data(TypedDict):
    invited_requests: list[InvitedRequest]
    join_requests: list[JoinRequest]

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupSystemMsg(ApiAction[Response]):
    """获取群系统消息"""

    action:str = field(init=False,default="get_group_system_msg")
