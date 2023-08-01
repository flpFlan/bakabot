"""群全员禁言"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetGroupWholeBan(ApiAction[ResponseBase]):
    """群全员禁言"""

    action:str = field(init=False,default="set_group_whole_ban")
    group_id: int
    enable: bool = True