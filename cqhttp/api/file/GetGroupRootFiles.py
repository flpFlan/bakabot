"""获取群根目录文件列表"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

@dataclass
class File:
    group_id: int
    file_id: str
    file_name: str
    busid: int
    file_size: int
    upload_time: int
    dead_time: int
    modify_time: int
    download_times: int
    uploader: int
    uploader_name: str

@dataclass
class Folder:
    group_id: int
    folder_id: str
    folder_name: str
    create_time: int
    creator: int
    creator_name: str
    total_file_count: int

class Data(TypedDict):
    files: list[File]
    folders: list[Folder]
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupRootFiles(ApiAction[Response]):
    """获取群根目录文件列表"""

    action:str = field(init=False,default="get_group_root_files")
    group_id: int