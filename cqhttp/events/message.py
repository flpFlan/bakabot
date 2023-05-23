from typing import Optional
from dataclasses import dataclass,field
from cqhttp.events.base import CQHTTPEvent

@dataclass
class Message(CQHTTPEvent):
    @dataclass
    class Sender:
        user_id: int = field(kw_only=True)
        nickname: str = field(kw_only=True)
        sex: str = field(kw_only=True)
        age: int = field(kw_only=True)

    post_type:str = "message"

    message_type: str = field(kw_only=True)
    sub_type: str = field(kw_only=True)
    message_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    message: str = field(kw_only=True)
    raw_message: str = field(kw_only=True)
    font: int = field(kw_only=True)
    sender: object = field(kw_only=True)
    message_sent:bool = field(default=False,kw_only=True)
    

@dataclass
class PrivateMessage(Message):
    """私聊消息"""

    message_type:str = "private"
    
    sender: Message.Sender = field(kw_only=True)
    target_id: int = field(kw_only=True)
    temp_source: int = field(kw_only=True)
    
    

@CQHTTPEvent.register
@dataclass
class FriendMessage(PrivateMessage):
    """好友消息"""

    sub_type:str = "friend"

@CQHTTPEvent.register
@dataclass
class GroupTempMessage(PrivateMessage):
    """群临时会话消息"""

    @dataclass
    class Sender(Message.Sender):
        group_id: int = field(kw_only=True)

    sub_type:str = "group"

    sender: Sender = field(kw_only=True)
    


@CQHTTPEvent.register
@dataclass
class GroupSelfMessage(PrivateMessage):
    """群中自身发送的消息"""

    sub_type:str = "group_self"


@CQHTTPEvent.register
@dataclass
class OtherMessage(PrivateMessage):
    """未分类的私聊消息"""

    sub_type:str = "other"


@dataclass
class GroupMessage(Message):
    """群消息"""

    @dataclass
    class Sender:
        user_id: int = field(kw_only=True)
        nickname: str = field(kw_only=True)
        sex: Optional[str] = field(default=None,kw_only=True)
        age: Optional[int] = field(default=None,kw_only=True)
        card: Optional[str] = field(default=None,kw_only=True)
        area: Optional[str] = field(default=None,kw_only=True)
        level: Optional[str] = field(default=None,kw_only=True)
        role: Optional[str] = field(default=None,kw_only=True)
        title: Optional[str] = field(default=None,kw_only=True)

    @dataclass
    class Anonymous:
        id: int = field(kw_only=True)
        name: str = field(kw_only=True)
        flag: str = field(kw_only=True)

    message_type:str = "group"

    sender: Sender = field(kw_only=True)
    group_id: int = field(kw_only=True)
    anonymous: Optional[Anonymous] = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class NormalMessage(GroupMessage):
    """正常消息"""

    sub_type:str = "normal"


@CQHTTPEvent.register
@dataclass
class AnonymousMessage(GroupMessage):
    """匿名消息"""

    sub_type:str = "anonymous"


@CQHTTPEvent.register
@dataclass
class NoticeMessage(GroupMessage):
    """系统提示 ( 如「管理员已禁止群内匿名聊天」 )"""

    sub_type:str = "notice"
