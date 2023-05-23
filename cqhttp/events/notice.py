from cqhttp.events.base import CQHTTPEvent
from dataclasses import dataclass,field

@dataclass
class Notice(CQHTTPEvent):
    post_type:str = "notice"

    notice_type: str = field(kw_only=True)

@CQHTTPEvent.register
@dataclass
class PrivateMessageRecalled(Notice):
    """私聊消息撤回"""

    notice_type:str = "friend_recall"

    user_id: int = field(kw_only=True)
    message_id: int = field(kw_only=True)

@CQHTTPEvent.register
@dataclass
class GroupMessageRecalled(Notice):
    """群消息撤回"""

    notice_type:str = "group_recall"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    operator_id: int = field(kw_only=True)
    message_id: int = field(kw_only=True)

@dataclass
class GroupMemberIncreased(Notice):
    """群成员增加"""

    notice_type:str = "group_increase"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    operator_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)

@dataclass
@CQHTTPEvent.register
class GroupMemberApproveIncreased(GroupMemberIncreased):
    """管理员已同意入群"""

    sub_type:str = "approve"


@CQHTTPEvent.register
@dataclass
class GroupMemberInviteIncreased(GroupMemberIncreased):
    """管理员邀请入群"""

    sub_type:str = "invite"

@dataclass
class GroupMemberDecreased(Notice):
    """群成员减少"""

    notice_type:str = "group_decrease"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    operator_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupMemberLeaveDecreased(GroupMemberDecreased):
    """主动退群"""

    sub_type :str = "leave"


@CQHTTPEvent.register
@dataclass
class GroupMemberKickDecreased(GroupMemberDecreased):
    """成员被踢"""

    sub_type :str = "kick"


@CQHTTPEvent.register
@dataclass
class GroupMemberKickMeDecreased(GroupMemberDecreased):
    """登录号被踢"""

    sub_type:str = "kick_me"

@dataclass
class GroupAdministratorChanged(Notice):
    """群管理员变动"""

    notice_type :str = "group_admin"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupAdministratorSet(GroupAdministratorChanged):
    """设置管理员"""

    sub_type :str = "set"


@CQHTTPEvent.register
@dataclass
class GroupAdministratorUnset(GroupAdministratorChanged):
    """取消管理员"""

    sub_type:str = "unset"


@CQHTTPEvent.register
@dataclass
class GroupFileUploaded(Notice):
    """群文件上传"""

    @dataclass
    class File:
        id: str = field(kw_only=True)
        name: str = field(kw_only=True)
        size: int = field(kw_only=True)
        busid: int = field(kw_only=True)

    notice_type:str = "group_upload"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    file: File = field(kw_only=True)

@dataclass
class GroupMemberBanOrLift(Notice):
    """群禁言"""

    notice_type:str = "group_ban"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    operator_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    duration: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupMemberBanned(GroupMemberBanOrLift):
    """禁言"""

    sub_type:str = "ban"


@CQHTTPEvent.register
@dataclass
class GroupMemberLiftBan(GroupMemberBanOrLift):
    """解除禁言"""

    sub_type:str = "lift_ban"


@CQHTTPEvent.register
@dataclass
class FriendAdded(Notice):
    """好友添加"""

    notice_type:str = "friend_add"

    user_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class PrivatePoked(Notice):
    """好友戳一戳（双击头像）"""

    notice_type :str = "notify"
    sub_type: str = "poke"

    sender_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    target_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupPoked(Notice):
    """群内戳一戳（双击头像）"""

    notice_type :str = "notify"
    sub_type: str = "poke"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    target_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupRedBagKingNotice(Notice):
    """群红包运气王提示"""

    notice_type :str = "notify"
    sub_type: str  = "lucky_king"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    target_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupMemberHonorChanged(Notice):
    """群成员荣誉变更提示"""

    notice_type :str = "notify"
    sub_type: str  = "honor"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    honor_type: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupMemberTitleChanged(Notice):
    """群成员头衔变更"""

    notice_type :str = "notify"
    sub_type: str  = "title"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    title: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupMemberCardRefreshed(Notice):
    """群成员名片更新"""

    notice_type :str = "group_card"

    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    card_new: str = field(kw_only=True)
    card_old: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class OfflineFileReceived(Notice):
    """接收到离线文件"""

    @dataclass
    class File:
        name: str = field(kw_only=True)
        size: int = field(kw_only=True)
        url: str = field(kw_only=True)

    notice_type :str = "offline_file"

    user_id: int = field(kw_only=True)
    file: File = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class ClientOnlineStateChanged(Notice):
    """其他客户端在线状态变更"""

    @dataclass
    class Device:
        app_id: int = field(kw_only=True)
        device_name: str = field(kw_only=True)
        device_kind: str = field(kw_only=True)

    notice_type:str = "client_status"

    client: Device = field(kw_only=True)
    online: bool = field(kw_only=True)

@dataclass
class EssentialMessageChanged(Notice):
    """精华消息变更"""

    notice_type:str = "essence"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    sender_id: int = field(kw_only=True)
    operator_id: int = field(kw_only=True)
    message_id: int = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class EssentialMessageAdded(EssentialMessageChanged):
    "精华消息添加"

    sub_type :str = "add"


@CQHTTPEvent.register
@dataclass
class EssentialMessageDeleted(EssentialMessageChanged):
    """精华消息移出"""

    sub_type :str = "delete"
