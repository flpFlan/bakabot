"""删除群文件文件夹"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteGroupFolder(ApiAction):
    """删除群文件文件夹"""

    action = "delete_group_folder"

    def __init__(self, group_id: int, folder_id: str, *, echo: Optional[str] = None):
        self.group_id = group_id
        self.folder_id = folder_id
        self.echo = echo
