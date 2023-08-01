"""处理加群请求／邀请"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    master_id: int
    ext_name: str
    create_time: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SetGroupAddRequest(ApiAction[Response]):
    """处理加群请求／邀请"""

    action:str = field(init=False,default="set_group_add_request")
    flag: str
    sub_type: str
    approve: bool = True
    reason: str = ""
