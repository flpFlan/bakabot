from typing import NotRequired, Optional, TypedDict
from .base import CQHTTPEvent


class MessageSender(TypedDict):
    user_id: int
    nickname: str
    sex: str
    age: int


class Message(CQHTTPEvent):
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: str
    raw_message: str
    font: int
    sender: MessageSender
    message_sent: NotRequired[bool]


class PrivateMessage(Message):
    target_id: int
    temp_source: int


class FriendMessage(PrivateMessage):
    pass


class GroupMessageSender(MessageSender):
    group_id: int


class GroupTempMessage(PrivateMessage):
    sender: GroupMessageSender


class GroupSelfMessage(PrivateMessage):
    pass


class OtherMessage(PrivateMessage):
    pass


class GroupMessageSender(TypedDict):
    user_id: int
    nickname: str
    sex: Optional[str]
    age: Optional[int]
    card: Optional[str]
    area: Optional[str]
    level: Optional[str]
    role: Optional[str]
    title: Optional[str]


class GroupMessage(Message):
    pass
