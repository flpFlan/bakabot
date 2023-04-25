"""处理加群请求／邀请"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        master_id: int
        ext_name: str
        create_time: int

    data: Data


@register_to_api
class SetGroupAddRequest(ApiAction[Response]):
    """处理加群请求／邀请"""

    action = "set_group_add_request"
    response: Response

    def __init__(
        self,
        flag: str,
        sub_type: str,
        approve: bool = True,
        reason: str = "",
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.flag = flag
        self.sub_type = sub_type
        self.approve = approve
        self.reason = reason
        self.echo = echo
