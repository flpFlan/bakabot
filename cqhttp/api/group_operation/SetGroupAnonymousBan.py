"""群匿名用户禁言"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.events.message import GroupMessage


@ApiAction.register
@dataclass
class SetGroupAnonymousBan(ApiAction[ResponseBase]):
    """群匿名用户禁言"""

    action:str = field(init=False,default="set_group_anonymous_ban")
    group_id: int
    anonymous: GroupMessage.Anonymous | None = None
    anonymous_flag: str = ""
    duration: int = 30 * 60
