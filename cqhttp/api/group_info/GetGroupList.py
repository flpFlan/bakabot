"""获取群列表"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase
from cqhttp.api.group_info.GetGroupInfo import Data

class Response(ResponseBase):
    data: list[Data]


@ApiAction.register
@dataclass
class GetGroupList(ApiAction[Response]):
    """获取群列表"""

    action:str = field(init=False,default="get_group_list")
    no_cache: bool = False
