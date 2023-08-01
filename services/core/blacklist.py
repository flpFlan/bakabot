# -- stdlib --
import logging

# -- third party --
# -- own --
from .base import CoreService
from services.base import ServiceBehavior, OnEvent, IMessageFilter
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage, Message
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.message.SendPrivateMsg import SendPrivateMsg
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.blacklist")
blacklist: set[int] = set()


class BlackList(CoreService):
    async def __setup(self):
        await ACCIO.db.execute(
            "create table if not exists blacklist (qq_number integer unique)"
        )

    async def get(self) -> set[int]:
        db = ACCIO.db
        await db.execute("select qq_number from blacklist")
        result = await db.fatchall()
        await db.commit()
        return set(group[0] for group in result)

    async def add(self, qq_number: int):
        if qq_number in blacklist:
            log.warning("try to add group_id already exist")
            return
        db = ACCIO.db

        await db.execute(
            f"insert into blacklist (qq_number) values (?)",
            (qq_number,),
        )
        await db.commit()
        blacklist.add(qq_number)

    async def delete(self, qq_number: int):
        if qq_number not in blacklist:
            log.warning("try to delete qq_number not exist")
            return
        await ACCIO.db.execute("delete from blacklist where qq_number = ?", (qq_number,))
        blacklist.remove(qq_number)


class Action(ServiceBehavior[BlackList], IMessageFilter):
    entrys = [r"^/(?P<action>ban|release) (?P<qq>\d+)"]

    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        if not (r := self.filter(evt)):
            return
        if not evt.user_id in ACCIO.bot.Administrators:
            return
        qq = int(r["qq"])
        if r["action"] == "ban":
            await self.service.add(qq)
            if isinstance(evt, GroupMessage):
                SendGroupMsg(evt.group_id, f"qq{qq}移至黑名单").forget()
            else:
                SendPrivateMsg(evt.user_id, f"qq{qq}移至黑名单").forget()
        elif r["action"] == "release":
            await self.service.delete(qq)
            if isinstance(evt, GroupMessage):
                SendGroupMsg(evt.group_id, f"qq{qq}移出黑名单").forget()
            else:
                SendPrivateMsg(evt.user_id, f"qq{qq}移出黑名单").forget()


class BlockUser(ServiceBehavior[BlackList]):
    async def __setup(self):
        global blacklist
        self.blacklist = blacklist = await self.service.get()

    @OnEvent[CQHTTPEvent].add_listener
    async def handle(self, evt: CQHTTPEvent):
        if user_id := getattr(evt, "user_id", None):
            if user_id in self.blacklist:
                evt.cancel()
