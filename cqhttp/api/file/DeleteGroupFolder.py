"""删除群文件文件夹"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class DeleteGroupFolder(ApiAction[ResponseBase]):
    """删除群文件文件夹"""

    action = "delete_group_folder"

    def __init__(self, group_id: int, folder_id: str, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.folder_id = folder_id
        self.echo = echo
