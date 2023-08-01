"""获取当前账号在线客户端列表"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Device(TypedDict):
    app_id: int
    device_name: str
    device_kind: str
    
class Response(ResponseBase):
    clients: list[Device]


@ApiAction.register
@dataclass
class GetOnlineClients(ApiAction[Response]):
    """获取当前账号在线客户端列表"""

    action:str = field(init=False,default="get_online_clients")
    no_cache: bool