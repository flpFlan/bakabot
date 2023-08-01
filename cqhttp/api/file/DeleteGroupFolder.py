"""删除群文件文件夹"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class DeleteGroupFolder(ApiAction[ResponseBase]):
    """删除群文件文件夹"""

    action:str = field(init=False,default="delete_group_folder")
    group_id: int
    folder_id: str
