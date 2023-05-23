"""创建群文件文件夹"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class CreateGroupFileFolder(ApiAction[ResponseBase]):
    """创建群文件文件夹"""

    action:str = field(init=False,default="create_group_file_folder")
    group_id: int
    name: str
    parent_id: str = "/"
