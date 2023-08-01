"""上传私聊文件"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class UploadPrivateFile(ApiAction[ResponseBase]):
    """上传私聊文件"""

    action:str = field(init=False,default="upload_private_file")
    user_id: int
    file: str
    name: str
