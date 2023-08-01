"""删除群文件"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class DeleteGroupFile(ApiAction[ResponseBase]):
    """删除群文件"""

    action:str = field(init=False,default="delete_group_file")
    group_id: int
    file_id: str
    busid: int
