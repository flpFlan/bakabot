"""设置群名"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,ResponseBase


@ApiAction.register
@dataclass
class SetGroupName(ApiAction[ResponseBase]):
    """设置群名"""

    action:str = field(init=False,default="set_group_name")
    group_id: int
    group_name: str
