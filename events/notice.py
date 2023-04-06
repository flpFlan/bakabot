from events.base import CQHTTPEvent


class Notice(CQHTTPEvent):
    post_type = "notice"
    notice_type: str


class PrivateMessageRecalled(Notice):
    """私聊消息撤回"""

    notice_type = "friend_recall"

    user_id: int
    message_id: int


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


class GroupMemberApproveIncreased(GroupMemberIncreased):
    """管理员已同意入群"""

    sub_type = "approve"


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


class GroupMemberLeaveDecreased(GroupMemberDecreased):
    """主动退群"""

    sub_type = "leave"


class GroupMemberKickDecreased(GroupMemberDecreased):
    """成员被踢"""

    sub_type = "kick"


class GroupMemberKickMeDecreased(GroupMemberDecreased):
    """登录号被踢"""

    sub_type = "kick_me"


class GroupAdministratorChanged(Notice):
    """群管理员变动"""

    notice_type = "group_admin"

    sub_type: str
    group_id: int
    user_id: int


class GroupAdministratorSet(GroupAdministratorChanged):
    """设置管理员"""

    sub_type = "set"


class GroupAdministratorUnset(GroupAdministratorChanged):
    """取消管理员"""

    sub_type = "unset"


class GroupFileUploaded(Notice):
    """群文件上传"""

    notice_type = "group_upload"

    group_id: int
    user_id: int
    file: dict


class GroupMemberBanOrLift(Notice):
    """群禁言"""

    notice_type = "group_ban"

    sub_type: str
    group_id: int
    operator_id: int
    user_id: int
    duration: int


class GroupMemberBanned(GroupMemberBanOrLift):
    """禁言"""

    sub_type = "ban"


class GroupMemberLiftBan(GroupMemberBanOrLift):
    """解除禁言"""

    sub_type = "lift_ban"


class FriendAdded(Notice):
    """好友添加"""

    notice_type = "friend_add"

    user_id: int


class PrivatePoked(Notice):
    """好友戳一戳（双击头像）"""

    notice_type = "notify"

    sub_type: str = "poke"
    sender_id: int
    user_id: int
    target_id: int


class GroupPoked(Notice):
    """群内戳一戳（双击头像）"""

    notice_type = "notify"

    sub_type: str = "poke"
    group_id: int
    user_id: int
    target_id: int


class GroupRedBagKingNotice(Notice):
    """群红包运气王提示"""

    notice_type = "notify"

    sub_type: str = "lucky_king"
    group_id: int
    user_id: int
    target_id: int


class GroupMemberHonorChanged(Notice):
    """群成员荣誉变更提示"""

    notice_type = "notify"

    sub_type: str = "honor"
    group_id: int
    user_id: int
    honor_type: str


class GroupMemberTitleChanged(Notice):
    """群成员头衔变更"""

    notice_type = "notify"

    sub_type: str = "title"
    group_id: int
    user_id: int
    title: str


class GroupMemberCardRefreshed(Notice):
    """群成员名片更新"""

    notice_type = "group_card"

    group_id: int
    user_id: int
    card_new: str
    card_old: str


class OfflineFileReceived(Notice):
    """接收到离线文件"""

    notice_type = "offline_file"

    user_id: int
    file: dict


class ClientOnlineStateChanged(Notice):
    """其他客户端在线状态变更"""

    notice_type = "client_status"

    client: dict
    online: bool


class EssentialMessageChanged(Notice):
    """精华消息变更"""

    notice_type = "essence"

    sub_type: str
    group_id: int
    sender_id: int
    operator_id: int
    message_id: int


class EssentialMessageAdded(EssentialMessageChanged):
    "精华消息添加"
    sub_type = "add"


class EssentialMessageDeleted(EssentialMessageChanged):
    """精华消息移出"""

    sub_type = "delete"
