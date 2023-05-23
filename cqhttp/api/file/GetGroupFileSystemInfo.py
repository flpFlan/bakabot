"""获取群文件系统信息"""
from dataclasses import dataclass,field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    file_count: int
    limit_count: int
    used_space: int
    total_space: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupFileSystemInfo(ApiAction[Response]):
    """获取群文件系统信息"""

    action:str = field(init=False,default="get_group_file_system_info")
    group_id: int