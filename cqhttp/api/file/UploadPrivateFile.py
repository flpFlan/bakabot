"""上传私聊文件"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class UploadPrivateFile(ApiAction[ResponseBase]):
    """上传私聊文件"""

    action = "upload_private_file"

    def __init__(
        self, user_id: int, file: str, name: str, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.user_id = user_id
        self.file = file
        self.name = name
        self.echo = echo
