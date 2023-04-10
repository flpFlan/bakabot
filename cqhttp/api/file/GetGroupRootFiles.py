"""获取群根目录文件列表"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


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


class Folder:
    group_id: int
    folder_id: str
    folder_name: str
    create_time: int
    creator: int
    creator_name: str
    total_file_count: int


class Response(ResponseBase):
    class Data:
        files: list[File]
        folders: list[Folder]

    data: Data


@register_to_api
class GetGroupRootFiles(ApiAction[Response]):
    """获取群根目录文件列表"""

    action = "get_group_root_files"
    response = Response()

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        self.group_id = group_id
        self.echo = echo
