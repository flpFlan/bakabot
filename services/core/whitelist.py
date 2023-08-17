# -- stdlib --
import logging
from typing import ClassVar, Self

# -- own --
from .base import CoreService
from services.base import OnEvent, ServiceBehavior, IMessageFilter
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage
from cqhttp.events.notice import GroupMemberBanned
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_operation.SetGroupLeave import SetGroupLeave
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.whitelist")
whitelist: set[int] = set()


class WhiteList(CoreService):
    instance: ClassVar[Self]

    async def __setup(self):
        WhiteList.instance = self
        await ACCIO.db.execute(
            "create table if not exists whitelist (group_id integer unique)"
        )

    async def get(self) -> set[int]:
        await ACCIO.db.execute("select group_id from whitelist")
        result = await ACCIO.db.fatchall()
        return set(group[0] for group in result)

    async def add(self, group_id: int):
        if group_id in whitelist:
            log.warning("try to add group_id already exist")
            return
        await ACCIO.db.execute(
            "insert into whitelist (group_id) values (?)", (group_id,)
        )
        whitelist.add(group_id)

    async def delete(self, group_id: int):
        if group_id not in whitelist:
            log.warning("try to delete group_id not exist")
            return
        await ACCIO.db.execute("delete from whitelist where group_id = ?", (group_id,))
        whitelist.remove(group_id)


class Manage(ServiceBehavior[WhiteList], IMessageFilter):
    entrys = [
        r"^(?P<action>/ping)\s+(?P<bot>.+)",
        r"^(?P<action>/delete)\s+(?P<bot>.+)",
        r"^(?P<action>/leave)$",
    ]

    @OnEvent[GroupMessage].add_listener
    async def ping(self, evt: GroupMessage):
        if evt.user_id not in ACCIO.bot.Administrators:
            return
        if not (r := self.filter(evt)):
            return

        match r["action"]:
            case "/ping":
                if not r["bot"] == ACCIO.bot.name:
                    return
                await self.service.add(evt.group_id)
                await SendGroupMsg(evt.group_id, "%s已在本群启用！" % ACCIO.bot.name).do()
            case "/delete":
                if not r["bot"] == ACCIO.bot.name:
                    return
                await self.service.delete(evt.group_id)
            case "/leave":
                await SetGroupLeave(evt.group_id).do()

    @OnEvent[GroupMemberBanned].add_listener
    async def leave(self, evt: GroupMemberBanned):
        if evt.user_id == ACCIO.bot.qq_number:
            await SetGroupLeave(evt.group_id).do()


class BlockGroup(ServiceBehavior[WhiteList]):
    async def __setup(self):
        global whitelist
        self.whitelist = whitelist = await self.service.get()

    @OnEvent[CQHTTPEvent].add_listener
    async def handle(self, evt: CQHTTPEvent):
        if group_id := getattr(evt, "group_id", None):
            if group_id not in self.whitelist:
                evt.cancel()
