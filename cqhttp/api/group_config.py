"""群设置相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupName(ApiAction):
    action = "set_group_name"

    def __init__(self, group_id: int, group_name: str, *, echo: str = ""):
        self.group_id = group_id
        self.group_name = group_name
        self.echo = echo


@register_to_api
class SetGroupPortrait(ApiAction):
    action = "set_group_portrait"

    def __init__(
        self, group_id: int, file: str, cache: int = 1, *, echo: str = ""
    ) -> None:
        self.group_id = group_id
        self.file = file
        self.cache = cache
        self.echo = echo


@register_to_api
class SetGroupAdmin(ApiAction):
    action = "set_group_admin"

    def __init__(
        self, group_id: int, user_id: int, enable: bool = True, *, echo: str = ""
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.enable = enable
        self.echo = echo


@register_to_api
class SetGroupCard(ApiAction):
    action = "set_group_card"

    def __init__(self, group_id: int, user_id: int, card: str = "", *, echo: str = ""):
        self.group_id = group_id
        self.user_id = user_id
        self.card = card
        self.echo = echo


@register_to_api
class SetGroupSpecialTitle(ApiAction):
    action = "set_group_special_title"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        special_title: str = "",
        duration: int = -1,
        *,
        echo: str = ""
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.special_title = special_title
        self.duration = duration
        self.echo = echo
