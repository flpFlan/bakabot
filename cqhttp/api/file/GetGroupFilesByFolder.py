from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.api.file.GetGroupRootFiles import File, Folder


class Response(ResponseBase):
    class Data:
        files: list[File]
        folders: list[Folder]

    data: Data


@register_to_api
class GetGroupFilesByFolder(ApiAction[Response]):
    """获取群子目录文件列表"""

    action = "get_group_files_by_folder"
    response = Response()

    def __init__(self, group_id: int, folder_id: str, *, echo: Optional[str] = None):
        self.group_id = group_id
        self.folder_id = folder_id
        self.echo = echo
