from typing import Optional
from cqhttp.events.base import CQHTTPEvent


class Message(CQHTTPEvent):
    class Sender:
        user_id: int
        nickname: str
        sex: str
        age: int

    post_type: str = "message"

    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: str
    raw_message: str
    font: int
    sender: Sender
#    message_sent:bool = field(default=False,kw_only=True)


class PrivateMessage(Message):
    """私聊消息"""

    message_type: str = "private"

    sender: Message.Sender
    target_id: int
    temp_source: int


@CQHTTPEvent.register
class FriendMessage(PrivateMessage):
    """好友消息"""

    sub_type: str = "friend"


@CQHTTPEvent.register
class GroupTempMessage(PrivateMessage):
    """群临时会话消息"""

    class Sender(Message.Sender):
        group_id: int

    sub_type: str = "group"

    sender: Sender


@CQHTTPEvent.register
class GroupSelfMessage(PrivateMessage):
    """群中自身发送的消息"""

    sub_type: str = "group_self"


@CQHTTPEvent.register
class OtherMessage(PrivateMessage):
    """未分类的私聊消息"""

    sub_type: str = "other"


class GroupMessage(Message):
    """群消息"""

    class Sender:
        user_id: int
        nickname: str
        sex: Optional[str]
        age: Optional[int]
        card: Optional[str]
        area: Optional[str]
        level: Optional[str]
        role: Optional[str]
        title: Optional[str]

    class Anonymous:
        id: int
        name: str
        flag: str

    message_type: str = "group"

    sender: Sender # type: ignore
    group_id: int
    anonymous: Optional[Anonymous]


@CQHTTPEvent.register
class NormalMessage(GroupMessage):
    """正常消息"""

    sub_type: str = "normal"


@CQHTTPEvent.register
class AnonymousMessage(GroupMessage):
    """匿名消息"""

    sub_type: str = "anonymous"


@CQHTTPEvent.register
class NoticeMessage(GroupMessage):
    """系统提示 ( 如「管理员已禁止群内匿名聊天」 )"""

    sub_type: str = "notice"
