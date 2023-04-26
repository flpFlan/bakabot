# -- stdlib --

# -- third party --
# -- own --
import asyncio
from cqhttp.api.message.SendPrivateMsg import SendPrivateMsg
from services.base import register_to, Service, EventHandler
from cqhttp.events.request import FriendRequest, GroupInviteRequest
from cqhttp.events.notice import GroupMemberIncreased, GroupMemberDecreased, FriendAdded
from cqhttp.api.message.SendMsg import SendMsg
from cqhttp.api.handle.SetFriendAddRequest import SetFriendAddRequest
from cqhttp.api.handle.SetGroupAddRequest import SetGroupAddRequest
from services.core.whitelist import WhiteList
from config import Administrators

# -- code --


class OnNewFriendGroupCore(EventHandler):
    interested = [FriendRequest, GroupInviteRequest, GroupMemberDecreased]

    async def handle(self, evt: FriendRequest | GroupInviteRequest):
        if isinstance(evt, GroupMemberDecreased):
            if not evt.user_id == self.bot.qq_number:
                return
            WhiteList.instance.delete(evt.group_id)
            m = f"{self.bot.name}已退出群聊\ngroup:\n{evt.group_id}\noperator:\n{evt.operator_id}\ncomment\n{evt.comment}"
            SendPrivateMsg.many(Administrators, m).do(self.bot)
            return

        if isinstance(evt, FriendRequest):
            m = f"有新的好友请求:\nuser:\n{evt.user_id}\ncomment:\n{evt.comment}"
            await SetFriendAddRequest(evt.flag, True).do(self.bot)
        elif isinstance(evt, GroupInviteRequest):
            m = f"有新的群聊邀请:\nuser:\n{evt.user_id}\ngroup:\n{evt.group_id}\ncomment:\n{evt.comment}"
            await SetGroupAddRequest(evt.flag, "invite", True).do(self.bot)

        SendPrivateMsg.many(Administrators, m).do(self.bot)


class OnNewFriendGroupEcho(EventHandler):
    interested = [GroupMemberIncreased, FriendAdded]

    async def handle(self, evt: GroupMemberIncreased | FriendAdded):
        if isinstance(evt, GroupMemberIncreased):
            if not evt.user_id == self.bot.qq_number:
                return
            m = "想让妾身为您服务的话，请联系[CQ:at,qq=2104357372]获取白名单"
            await SendMsg(group_id=evt.group_id, message=m).do(self.bot)
        if isinstance(evt, FriendAdded):
            m = "想让妾身为您服务的话，请邀请妾身到相关的群内，并联系master (2104357372)获取白名单"
            await SendMsg(user_id=evt.user_id, message=m).do(self.bot)


@register_to("ALL")
class OnNewFriendGroup(Service):
    cores = [OnNewFriendGroupCore, OnNewFriendGroupEcho]
