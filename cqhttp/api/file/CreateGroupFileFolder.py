"""创建群文件文件夹"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class CreateGroupFileFolder(ApiAction[ResponseBase]):
    """创建群文件文件夹"""

    action = "create_group_file_folder"

    def __init__(
        self,
        group_id: int,
        name: str,
        parent_id: str = "/",
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.name = name
        self.parent_id = parent_id
        self.echo = echo
