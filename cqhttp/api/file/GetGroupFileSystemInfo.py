"""获取群文件系统信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        file_count: int
        limit_count: int
        used_space: int
        total_space: int

    data: Data


@register_to_api
class GetGroupFileSystemInfo(ApiAction[Response]):
    """获取群文件系统信息"""

    action = "get_group_file_system_info"
    response: Response

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.echo = echo
