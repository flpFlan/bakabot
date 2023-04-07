from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import register_to_events


class Notice(CQHTTPEvent):
    post_type = "notice"
    notice_type: str


@register_to_events
class PrivateMessageRecalled(Notice):
    """私聊消息撤回"""

    notice_type = "friend_recall"

    user_id: int
    message_id: int


@register_to_events
class GroupMessageRecalled(Notice):
    """群消息撤回"""

    notice_type = "group_recall"

    group_id: int
    user_id: int
    operator_id: int
    message_id: int


class GroupMemberIncreased(Notice):
    """群成员增加"""

    notice_type = "group_increase"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int


@register_to_events
class GroupMemberApproveIncreased(GroupMemberIncreased):
    """管理员已同意入群"""

    sub_type = "approve"


@register_to_events
class GroupMemberInviteIncreased(GroupMemberIncreased):
    """管理员邀请入群"""

    sub_type = "invite"


class GroupMemberDecreased(Notice):
    """群成员减少"""

    notice_type = "group_decrease"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int


@register_to_events
class GroupMemberLeaveDecreased(GroupMemberDecreased):
    """主动退群"""

    sub_type = "leave"


@register_to_events
class GroupMemberKickDecreased(GroupMemberDecreased):
    """成员被踢"""

    sub_type = "kick"


@register_to_events
class GroupMemberKickMeDecreased(GroupMemberDecreased):
    """登录号被踢"""

    sub_type = "kick_me"


class GroupAdministratorChanged(Notice):
    """群管理员变动"""

    notice_type = "group_admin"

    sub_type: str
    group_id: int
    user_id: int


@register_to_events
class GroupAdministratorSet(GroupAdministratorChanged):
    """设置管理员"""

    sub_type = "set"


@register_to_events
class GroupAdministratorUnset(GroupAdministratorChanged):
    """取消管理员"""

    sub_type = "unset"


@register_to_events
class GroupFileUploaded(Notice):
    """群文件上传"""

    class File:
        id: str
        name: str
        size: int
        busid: int

    notice_type = "group_upload"

    group_id: int
    user_id: int
    file: File


class GroupMemberBanOrLift(Notice):
    """群禁言"""

    notice_type = "group_ban"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int
    duration: int


@register_to_events
class GroupMemberBanned(GroupMemberBanOrLift):
    """禁言"""

    sub_type = "ban"


@register_to_events
class GroupMemberLiftBan(GroupMemberBanOrLift):
    """解除禁言"""

    sub_type = "lift_ban"


@register_to_events
class FriendAdded(Notice):
    """好友添加"""

    notice_type = "friend_add"

    user_id: int


@register_to_events
class PrivatePoked(Notice):
    """好友戳一戳（双击头像）"""

    notice_type = "notify"

    sub_type: str = "poke"
    sender_id: int
    user_id: int
    target_id: int


@register_to_events
class GroupPoked(Notice):
    """群内戳一戳（双击头像）"""

    notice_type = "notify"

    sub_type: str = "poke"
    group_id: int
    user_id: int
    target_id: int


@register_to_events
class GroupRedBagKingNotice(Notice):
    """群红包运气王提示"""

    notice_type = "notify"

    sub_type: str = "lucky_king"
    group_id: int
    user_id: int
    target_id: int


@register_to_events
class GroupMemberHonorChanged(Notice):
    """群成员荣誉变更提示"""

    notice_type = "notify"

    sub_type: str = "honor"
    group_id: int
    user_id: int
    honor_type: str


@register_to_events
class GroupMemberTitleChanged(Notice):
    """群成员头衔变更"""

    notice_type = "notify"

    sub_type: str = "title"
    group_id: int
    user_id: int
    title: str


@register_to_events
class GroupMemberCardRefreshed(Notice):
    """群成员名片更新"""

    notice_type = "group_card"

    group_id: int
    user_id: int
    card_new: str
    card_old: str


@register_to_events
class OfflineFileReceived(Notice):
    """接收到离线文件"""

    class File:
        name: str
        size: int
        url: str

    notice_type = "offline_file"

    user_id: int
    file: File


@register_to_events
class ClientOnlineStateChanged(Notice):
    """其他客户端在线状态变更"""

    class Device:
        app_id: int
        device_name: str
        device_kind: str

    notice_type = "client_status"

    client: Device
    online: bool


class EssentialMessageChanged(Notice):
    """精华消息变更"""

    notice_type = "essence"

    sub_type: str
    group_id: int
    sender_id: int
    operator_id: int
    message_id: int


@register_to_events
class EssentialMessageAdded(EssentialMessageChanged):
    "精华消息添加"
    sub_type = "add"


@register_to_events
class EssentialMessageDeleted(EssentialMessageChanged):
    """精华消息移出"""

    sub_type = "delete"
