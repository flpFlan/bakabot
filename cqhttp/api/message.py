"""有关消息操作的 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SendPrivateMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            message_id: int

        data: Data

    action = "send_private_msg"

    def __init__(
        self, user_id: int, group_id: int, message: str, auto_escape: bool = False
    ):
        self.user_id = user_id
        self.group_id = group_id
        self.message = message
        self.auto_escape = auto_escape


@register_to_api
class SendGroupMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            message_id: int

        data: Data

    action = "send_group_msg"

    def __init__(self, group_id: int, message: str, auto_escape: bool = False):
        self.group_id = group_id
        self.message = message
        self.auto_escape = auto_escape


@register_to_api
class SendMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            message_id: int

        data: Data

    action = "send_msg"

    def __init__(
        self,
        message_type: str,
        user_id: int,
        group_id: int,
        message: str,
        auto_escape: bool = False,
    ):
        self.message_type = message_type
        self.user_id = user_id
        self.group_id = group_id
        self.message = message


@register_to_api
class GetMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            class Sender:
                nickname: str
                user_id: int

            group: bool
            group_id: int | None = None
            message_id: int
            real_id: int
            message_type: str
            sender: Sender
            time: int
            message: str
            raw_message: str

        data: Data

    action = "get_msg"

    def __init__(self, message_id: int):
        self.message_id = message_id


@register_to_api
class DeleteMsg(ApiAction):
    action = "delete_msg"

    def __init__(self, message_id: int):
        self.message_id = message_id


class MarkMsgAsRead(ApiAction):
    action = "mark_msg_as_read"

    def __init__(self, message_id: int):
        self.message_id = message_id


@register_to_api
class GetForwardMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            messages: list

        data: Data

    action = "get_forward_msg"

    def __init__(self, message_id: int):
        self.message_id = message_id


@register_to_api
class SendGroupForwardMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            message_id: int
            forward_id: str

        data: Data

    action = "send_group_forward_msg"

    def __init__(self, group_id: int, messages: list):
        self.group_id = group_id
        self.messages = messages


@register_to_api
class SendPrivateForwardMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            message_id: int
            forward_id: str

        data: Data

    action = "send_private_forward_msg"

    def __init__(self, user_id: int, messages: list):
        self.user_id = user_id
        self.messages = messages


@register_to_api
class GetGroupMsgHistory(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            messages: list

        data: Data

    action = "get_group_msg_history"

    def __init__(self, message_seq: int, group_id: int):
        self.message_seq = message_seq
        self.group_id = group_id
