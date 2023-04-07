"""有关 Bot 账号的相关 API"""

from cqhttp.api.base import ApiAction


class GetLoginInfo(ApiAction):
    def __init__(self, action, echo=""):
        self.action = action
        self.echo = echo
