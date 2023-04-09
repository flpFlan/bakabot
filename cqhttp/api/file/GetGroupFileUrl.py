from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        url: str

    data: Data


@register_to_api
class GetGroupFileUrl(ApiAction[Response]):
    """获取群文件资源链接"""

    action = "get_group_file_url"
    response = Response()

    def __init__(
        self, group_id: int, file_id: str, busid: int, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.file_id = file_id
        self.busid = busid
        self.echo = echo
