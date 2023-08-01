"""发送群公告"""
from dataclasses import dataclass, field
from typing import Optional
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SendGroupNotice(ApiAction[ResponseBase]):
    """发送群公告"""

    action:str = field(init=False,default="_send_group_notice")
    group_id: int
    content: str
    image: Optional[str] = None
