# -- stdlib --
import logging

# -- third party --
from sqlalchemy import select, insert, delete

# -- own --
from .base import CoreService
from services.base import ServiceBehavior, OnEvent, IMessageFilter
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage, Message
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.message.SendPrivateMsg import SendPrivateMsg
from db.models.service import BlackList as BlackListModel
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.blacklist")
blacklist: set[int] = set()


class BlackList(CoreService):

    async def get(self) -> set[int]:
        async with ACCIO.db.session.begin():
            result = (await ACCIO.db.session.scalars(select(BlackListModel.qq_number))).all()
        return set(r for r in result)

    async def add(self, qq_number: int):
        if qq_number in blacklist:
            log.warning("try to add group_id already exist")
            return
        session = ACCIO.db.session

        async with session.begin():
            session.add(BlackListModel(qq_number=qq_number))
        blacklist.add(qq_number)

    async def delete(self, qq_number: int):
        if qq_number not in blacklist:
            log.warning("try to delete qq_number not exist")
            return
        session = ACCIO.db.session

        async with session.begin():
            await session.execute(delete(BlackListModel).where(BlackListModel.qq_number == qq_number))
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
