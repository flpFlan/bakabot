"""获取群文件资源链接"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    url: str
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupFileUrl(ApiAction[Response]):
    """获取群文件资源链接"""

    action:str = field(init=False,default="get_group_file_url")
    group_id: int
    file_id: str
    busid: int
