"""设置登录号资料"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetQQProfile(ApiAction):
    """设置登录号资料"""

    action = "set_qq_profile"

    def __init__(
        self,
        nickname: Optional[str] = None,
        company: Optional[str] = None,
        email: Optional[str] = None,
        college: Optional[str] = None,
        personal_note: Optional[str] = None,
        *,
        echo: Optional[str] = None
    ):
        self.nickname = nickname
        self.company = company
        self.email = email
        self.college = college
        self.personal_note = personal_note
        self.echo = echo
