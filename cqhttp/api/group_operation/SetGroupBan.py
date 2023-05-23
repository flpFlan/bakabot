"""群单人禁言"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,ResponseBase


@ApiAction.register
@dataclass
class SetGroupBan(ApiAction[ResponseBase]):
    """群单人禁言"""

    action:str = field(init=False,default="set_group_ban")
    group_id: int
    user_id: int
    duration: int = 30 * 60
