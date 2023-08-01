"""设置登录号资料"""
from dataclasses import dataclass, field
from typing import Optional
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetQQProfile(ApiAction[ResponseBase]):
    """设置登录号资料"""

    action:str = field(init=False,default="set_qq_profile")
    nickname: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    college: Optional[str] = None
    personal_note: Optional[str] = None