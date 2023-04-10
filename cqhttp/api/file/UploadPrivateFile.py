"""上传私聊文件"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class UploadPrivateFile(ApiAction):
    """上传私聊文件"""

    action = "upload_private_file"

    def __init__(
        self, user_id: int, file: str, name: str, *, echo: Optional[str] = None
    ):
        self.user_id = user_id
        self.file = file
        self.name = name
        self.echo = echo
