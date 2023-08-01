"""获取群子目录文件列表"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.api.file.GetGroupRootFiles import File, Folder

class Data(TypedDict):
    files: list[File]
    folders: list[Folder]

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupFilesByFolder(ApiAction[Response]):
    """获取群子目录文件列表"""

    action:str = field(init=False,default="get_group_files_by_folder")
    group_id: int
    folder_id: str
