"""删除群文件"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteGroupFile(ApiAction):
    """删除群文件"""

    action = "delete_group_file"

    def __init__(
        self, group_id: int, file_id: str, busid: int, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.file_id = file_id
        self.busid = busid
        self.echo = echo
