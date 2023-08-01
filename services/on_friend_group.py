# -- own --
from cqhttp.api.message.SendPrivateMsg import SendPrivateMsg
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.request import FriendRequest, GroupInviteRequest
from cqhttp.events.notice import GroupMemberIncreased, GroupMemberDecreased, FriendAdded
from cqhttp.api.message.SendMsg import SendMsg
from cqhttp.api.handle.SetFriendAddRequest import SetFriendAddRequest
from cqhttp.api.handle.SetGroupAddRequest import SetGroupAddRequest
from services.core.whitelist import WhiteList
from cqhttp.cqcode import At
from accio import ACCIO

# -- code --


class OnFriendGroup(Service):
    pass


class OnFriendGroupCore(ServiceBehavior[OnFriendGroup]):
    @OnEvent[FriendRequest, GroupInviteRequest].add_listener
    async def on_request(self, evt: FriendRequest | GroupInviteRequest):
        if isinstance(evt, FriendRequest):
            m = f"有新的好友请求:\nuser:\n{evt.user_id}\ncomment:\n{evt.comment}"
            await SetFriendAddRequest(evt.flag, True).do()
        elif isinstance(evt, GroupInviteRequest):
            m = f"有新的群聊邀请:\nuser:\n{evt.user_id}\ngroup:\n{evt.group_id}\ncomment:\n{evt.comment}"
            await SetGroupAddRequest(evt.flag, "invite", True).do()

        SendPrivateMsg.many(ACCIO.bot.Administrators, m).forget()

    @OnEvent[GroupMemberDecreased].add_listener
    async def on_member_decreased(self, evt: GroupMemberDecreased):
        if not evt.user_id == ACCIO.bot.qq_number:
            return
        await WhiteList.instance.delete(evt.group_id)
        m = f"{ACCIO.bot.name}已退出群聊\ngroup:\n{evt.group_id}\noperator:\n{evt.operator_id}"

        SendPrivateMsg.many(ACCIO.bot.Administrators, m).forget()


class OnFriendGroupEcho(ServiceBehavior[OnFriendGroup]):
    async def __setup(self):
        self.staff=ACCIO.conf.getint("Service.OnFriendGroupEcho", "staff")

    @OnEvent[GroupMemberIncreased, FriendAdded].add_listener
    async def handle(self, evt: GroupMemberIncreased | FriendAdded):
        if isinstance(evt, GroupMemberIncreased):
            if not evt.user_id == ACCIO.bot.qq_number:
                return
            m = f"想让妾身为您服务的话，请联系{At(self.staff)}获取白名单"
            await SendMsg(group_id=evt.group_id, message=m).do()
        elif isinstance(evt, FriendAdded):
            m = f"想让妾身为您服务的话，请邀请妾身到相关的群内，并联系{self.staff}获取白名单"
            await SendMsg(user_id=evt.user_id, message=m).do()
