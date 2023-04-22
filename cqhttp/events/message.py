from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import register_to_events


class Message(CQHTTPEvent):
    post_type = "message"
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: str
    raw_message: str
    font: int
    sender: object
    message_sent: bool = False

    def __init__(self):
        super().__init__()


class PrivateMessage(Message):
    """私聊消息"""

    class Sender:
        user_id: int
        nickname: str
        sex: str
        age: int

    message_type = "private"

    sender: Sender
    target_id: int
    temp_source: int

    def __init__(self):
        super().__init__()


@register_to_events
class FriendMessage(PrivateMessage):
    """好友消息"""

    sub_type = "friend"

    def __init__(self):
        super().__init__()


@register_to_events
class GroupTempMessage(PrivateMessage):
    """群临时会话消息"""

    class Sender(PrivateMessage.Sender):
        group_id: int

    sender: Sender
    sub_type = "group"

    def __init__(self):
        super().__init__()


@register_to_events
class GroupSelfMessage(PrivateMessage):
    """群中自身发送的消息"""

    sub_type = "group_self"

    def __init__(self):
        super().__init__()


@register_to_events
class OtherMessage(PrivateMessage):
    """未分类的私聊消息"""

    sub_type = "other"

    def __init__(self):
        super().__init__()


class GroupMessage(Message):
    """群消息"""

    class Sender:
        user_id: int
        nickname: str
        sex: str
        age: int
        card: str
        area: str
        level: str
        role: str
        title: str

    class Anonymous:
        id: int
        name: str
        flag: str

    message_type = "group"

    sender: Sender
    group_id: int
    anonymous: Anonymous | None

    def __init__(self):
        super().__init__()


@register_to_events
class NormalMessage(GroupMessage):
    """正常消息"""

    sub_type = "normal"

    def __init__(self):
        super().__init__()


@register_to_events
class AnonymousMessage(GroupMessage):
    """匿名消息"""

    sub_type = "anonymous"

    def __init__(self):
        super().__init__()


@register_to_events
class NoticeMessage(GroupMessage):
    """系统提示 ( 如「管理员已禁止群内匿名聊天」 )"""

    sub_type = "notice"

    def __init__(self):
        super().__init__()
