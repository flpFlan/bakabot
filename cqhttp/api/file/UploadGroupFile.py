"""上传群文件"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class UploadGroupFile(ApiAction[ResponseBase]):
    """上传群文件"""

    action = "upload_group_file"

    def __init__(
        self,
        group_id: int,
        file: str,
        name: str,
        folder: Optional[str] = None,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.file = file
        self.name = name
        if folder:
            self.folder = folder
        self.echo = echo
