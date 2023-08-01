"""上传群文件"""
from dataclasses import dataclass, field
from typing import Optional
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class UploadGroupFile(ApiAction[ResponseBase]):
    """上传群文件"""

    action:str = field(init=False,default="upload_group_file")
    group_id: int
    file: str
    name: str
    folder: Optional[str] = None
