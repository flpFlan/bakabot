"""群操作相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupBan(ApiAction):
    action = "set_group_ban"

    def __init__(
        self, group_id: int, user_id: int, duration: int = 30 * 60, *, echo: str = ""
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.duration = duration
        self.echo = echo


@register_to_api
class SetGroupWholeBan(ApiAction):
    action = "set_group_whole_ban"

    def __init__(self, group_id: int, enable: bool = True, *, echo: str = ""):
        self.group_id = group_id
        self.enable = enable
        self.echo = echo


@register_to_api
class SetGroupAnonymousBan(ApiAction):
    action = "set_group_anonymous_ban"

    def __init__(
        self,
        group_id: int,
        *,
        anonymous: object = None,
        anonymous_flag: str = "",
        duration: int = 30 * 60,
        echo: str = ""
    ):
        self.group_id = group_id
        assert anonymous or anonymous_flag, "anonymous和anonymous_flag必须传入一个"
        if anonymous:
            self.anonymous = anonymous
        if anonymous_flag:
            self.anonymous_flag = anonymous_flag
        self.duration = duration
        self.echo = echo


@register_to_api
class SetEssenceMsg(ApiAction):
    action = "set_essence_msg"

    def __init__(self, message_id: int, *, echo: str = ""):
        self.message_id = message_id
        self.echo = echo


@register_to_api
class DeleteEssenceMsg(ApiAction):
    action = "delete_essence_msg"

    def __init__(self, message_id: int, *, echo: str = ""):
        self.message_id = message_id
        self.echo = echo


@register_to_api
class SendGroupSign(ApiAction):
    action = "send_group_sign"

    def __init__(self, group_id: int, *, echo: str = ""):
        self.message_id = group_id
        self.echo = echo


@register_to_api
class SetGroupAnonymous(ApiAction):
    action = "set_group_anonymous"

    def __init__(self, group_id: int, enable: bool = True, *, echo: str = ""):
        self.group_id = group_id
        self.enable = enable
        self.echo = echo


@register_to_api
class SendGroupNotice(ApiAction):
    action = "_send_group_notice"

    def __init__(self, group_id: int, content: str, image: str = "", *, echo: str = ""):
        self.group_id = group_id
        self.content = content
        if image:
            self.image = image
        self.echo = echo


@register_to_api
class GetGroupNotice(ApiAction):
    class Response(ApiAction.Response):
        data: list

    action = "_get_group_notice"

    def __init__(self, group_id: int, *, echo: str = ""):
        self.group_id = group_id
        self.echo = echo


@register_to_api
class SetGroupKick(ApiAction):
    action = "set_group_kick"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        reject_add_request: bool = False,
        *,
        echo: str = ""
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.reject_add_request = reject_add_request
        self.echo = echo


@register_to_api
class SetGroupLeave(ApiAction):
    action = "set_group_leave"

    def __init__(self, group_id: int, is_dismiss: bool = False, *, echo: str = ""):
        self.group_id = group_id
        self.is_dismiss = is_dismiss
        self.echo = echo
