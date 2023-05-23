"""退出群组"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetGroupLeave(ApiAction[ResponseBase]):
    """退出群组"""

    action:str = field(init=False,default="set_group_leave")
    group_id: int
    is_dismiss: bool = False
