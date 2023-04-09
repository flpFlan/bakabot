from typing import Optional
from cqhttp.api.base import ApiAction, ResponseBase, register_to_api


class Response(ResponseBase):
    class Device:
        app_id: int
        device_name: str
        device_kind: str

    clients: list[Device]


@register_to_api
class GetOnlineClients(ApiAction[Response]):
    """获取当前账号在线客户端列表"""

    action = "get_online_clients"
    response = Response()

    def __init__(self, no_cache: bool, *, echo: Optional[str] = None):
        self.no_cache = no_cache
        self.echo = echo
