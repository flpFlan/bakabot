from cqhttp.events.base import CQHTTPEvent


class Notice(CQHTTPEvent):
    post_type: str = "notice"

    notice_type: str


@CQHTTPEvent.register
class PrivateMessageRecalled(Notice):
    """私聊消息撤回"""

    notice_type: str = "friend_recall"

    user_id: int
    message_id: int


@CQHTTPEvent.register
class GroupMessageRecalled(Notice):
    """群消息撤回"""

    notice_type: str = "group_recall"

    group_id: int
    user_id: int
    operator_id: int
    message_id: int


class GroupMemberIncreased(Notice):
    """群成员增加"""

    notice_type: str = "group_increase"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int


@CQHTTPEvent.register
class GroupMemberApproveIncreased(GroupMemberIncreased):
    """管理员已同意入群"""

    sub_type: str = "approve"


@CQHTTPEvent.register
class GroupMemberInviteIncreased(GroupMemberIncreased):
    """管理员邀请入群"""

    sub_type: str = "invite"


class GroupMemberDecreased(Notice):
    """群成员减少"""

    notice_type: str = "group_decrease"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int


@CQHTTPEvent.register
class GroupMemberLeaveDecreased(GroupMemberDecreased):
    """主动退群"""

    sub_type: str = "leave"


@CQHTTPEvent.register
class GroupMemberKickDecreased(GroupMemberDecreased):
    """成员被踢"""

    sub_type: str = "kick"


@CQHTTPEvent.register
class GroupMemberKickMeDecreased(GroupMemberDecreased):
    """登录号被踢"""

    sub_type: str = "kick_me"


class GroupAdministratorChanged(Notice):
    """群管理员变动"""

    notice_type: str = "group_admin"

    sub_type: str
    group_id: int
    user_id: int


@CQHTTPEvent.register
class GroupAdministratorSet(GroupAdministratorChanged):
    """设置管理员"""

    sub_type: str = "set"


@CQHTTPEvent.register
class GroupAdministratorUnset(GroupAdministratorChanged):
    """取消管理员"""

    sub_type: str = "unset"


@CQHTTPEvent.register
class GroupFileUploaded(Notice):
    """群文件上传"""

    class File:
        id: str
        name: str
        size: int
        busid: int

    notice_type: str = "group_upload"

    group_id: int
    user_id: int
    file: File


class GroupMemberBanOrLift(Notice):
    """群禁言"""

    notice_type: str = "group_ban"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int
    duration: int


@CQHTTPEvent.register
class GroupMemberBanned(GroupMemberBanOrLift):
    """禁言"""

    sub_type: str = "ban"


@CQHTTPEvent.register
class GroupMemberLiftBan(GroupMemberBanOrLift):
    """解除禁言"""

    sub_type: str = "lift_ban"


@CQHTTPEvent.register
class FriendAdded(Notice):
    """好友添加"""

    notice_type: str = "friend_add"

    user_id: int


#FIXME
@CQHTTPEvent.register
class PrivatePoked(Notice):
    """好友戳一戳（双击头像）"""

    notice_type: str = "notify"
    sub_type: str = "poke"

    sender_id: int
    user_id: int
    target_id: int


@CQHTTPEvent.register
class GroupPoked(Notice):
    """群内戳一戳（双击头像）"""

    notice_type: str = "notify"
    sub_type: str = "poke"

    group_id: int
    user_id: int
    target_id: int


@CQHTTPEvent.register
class GroupRedBagKingNotice(Notice):
    """群红包运气王提示"""

    notice_type: str = "notify"
    sub_type: str = "lucky_king"

    group_id: int
    user_id: int
    target_id: int


@CQHTTPEvent.register
class GroupMemberHonorChanged(Notice):
    """群成员荣誉变更提示"""

    notice_type: str = "notify"
    sub_type: str = "honor"

    group_id: int
    user_id: int
    honor_type: str


@CQHTTPEvent.register
class GroupMemberTitleChanged(Notice):
    """群成员头衔变更"""

    notice_type: str = "notify"
    sub_type: str = "title"

    group_id: int
    user_id: int
    title: str


@CQHTTPEvent.register
class GroupMemberCardRefreshed(Notice):
    """群成员名片更新"""

    notice_type: str = "group_card"

    group_id: int
    user_id: int
    card_new: str
    card_old: str


@CQHTTPEvent.register
class OfflineFileReceived(Notice):
    """接收到离线文件"""

    class File:
        name: str
        size: int
        url: str

    notice_type: str = "offline_file"

    user_id: int
    file: File


@CQHTTPEvent.register
class ClientOnlineStateChanged(Notice):
    """其他客户端在线状态变更"""

    class Device:
        app_id: int
        device_name: str
        device_kind: str

    notice_type: str = "client_status"

    client: Device
    online: bool


class EssentialMessageChanged(Notice):
    """精华消息变更"""

    notice_type: str = "essence"

    sub_type: str
    group_id: int
    sender_id: int
    operator_id: int
    message_id: int


@CQHTTPEvent.register
class EssentialMessageAdded(EssentialMessageChanged):
    "精华消息添加"

    sub_type: str = "add"


@CQHTTPEvent.register
class EssentialMessageDeleted(EssentialMessageChanged):
    """精华消息移出"""

    sub_type: str = "delete"
