"""群组踢人"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetGroupKick(ApiAction[ResponseBase]):
    """群组踢人"""

    action:str = field(init=False,default="set_group_kick")
    group_id: int
    user_id: int
    reject_add_request: bool = False
