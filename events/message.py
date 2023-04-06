from .base import CQHTTPEvent


class Message(CQHTTPEvent):
    post_type = "message"
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: str
    raw_message: str
    font: int
    sender: dict
    message_sent: bool = False


class PrivateMessage(Message):
    """私聊消息"""

    message_type = "private"

    target_id: int
    temp_source: int


class FriendMessage(PrivateMessage):
    """好友消息"""

    sub_type = "friend"


class GroupTempMessage(PrivateMessage):
    """群临时会话消息"""

    sub_type = "group"


class GroupSelfMessage(PrivateMessage):
    """群中自身发送的消息"""

    sub_type = "group_self"


class OtherMessage(PrivateMessage):
    """未分类的私聊消息"""

    sub_type = "other"


class GroupMessage(Message):
    """群消息"""

    message_type = "group"

    group_id: int
    anonymous: dict | None


class NormalMessage(GroupMessage):
    """正常消息"""

    sub_type = "normal"


class AnonymousMessage(GroupMessage):
    """匿名消息"""

    sub_type = "anonymous"


class NoticeMessage(GroupMessage):
    """系统提示 ( 如「管理员已禁止群内匿名聊天」 )"""

    sub_type = "notice"
