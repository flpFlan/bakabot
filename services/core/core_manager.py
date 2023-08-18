# -- stdlib --
import logging
from typing import ClassVar, Self

# -- third party --
# -- own --
from .base import CoreService
from services.base import ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events import CQHTTPEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.coreManager")


class CoreManager(CoreService):
    pass


class BotControl(ServiceBehavior[CoreManager], IMessageFilter):
    entrys = [r"^/bot on$", r"^/bot off$"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (
            evt.sender.role in ("owner", "admin")
            or evt.user_id in ACCIO.bot.Administrators
        ):
            return
        msg = evt.message
        group_id = evt.group_id
        if msg == "/bot on":
            await BlockGroup.instance.delete(group_id)
            await SendGroupMsg(group_id, f"{ACCIO.bot.name} running！").do()
        if msg == "/bot off":
            await BlockGroup.instance.add(group_id)
            c = SendGroupMsg(group_id, f"{ACCIO.bot.name} closed")
            await c.do()


class ServiceControl(ServiceBehavior[CoreManager], IMessageFilter):
    entrys = [
        r"^/(?P<get>get)$",
        r"^/close (?P<service_to_close>.+)",
        r"^/start (?P<service_to_start>.+)",
        r"^/help (?P<service>.+)",
    ]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (rslt := self.filter(evt)):
            return
        r = rslt.groupdict()
        if r.get("get"):
            await SendGroupMsg(evt.group_id, self.get_all_services()).do()
        elif s := r.get("service"):
            await SendGroupMsg(evt.group_id, self.get_help(s)).do()
        elif s := r.get("service_to_close"):
            if not evt.user_id in ACCIO.bot.Administrators:
                return
            await self.close_service(evt.group_id, s)
        elif s := r.get("service_to_start"):
            if not evt.user_id in ACCIO.bot.Administrators:
                return
            await self.start_service(evt.group_id, s)

    def get_all_services(self):
        # FIXME: missing condition: whether the service is blocked in this group
        l = [
            f"{service.name}: {'🟢'if service.get_activity()else '🔴'}"
            for service in ACCIO.bot.services
        ]
        return "\n".join(l)

    def get_help(self, service):
        for s in ACCIO.bot.services:
            if s.name.lower() == service.lower():
                return s.doc
        return "Unknown service"

    async def close_service(self, group_id, service):
        #TODO: ban service individually
        to_close = [s for s in ACCIO.bot.services if s.name == service]
        if not to_close:
            await SendGroupMsg(group_id, "Unknown service").do()
            return
        for s in to_close:
            if not s.get_activity():
                await SendGroupMsg(group_id, f"{service}已处于关闭状态！").do()
                continue
            await s.shutdown()
            await SendGroupMsg(group_id, f"{service}已关闭！").do()

    async def start_service(self, group_id, service):
        to_start = [s for s in ACCIO.bot.services if s.name == service]
        if not to_start:
            await SendGroupMsg(group_id, "Unknown service").do()
            return
        for s in to_start:
            if s.get_activity():
                await SendGroupMsg(group_id, f"{service}已处于启动状态！").do()
                continue
            await s.start()
            await SendGroupMsg(group_id, f"{service}已启动！").do()


class BlockGroup(ServiceBehavior[CoreManager]):
    instance: ClassVar[Self]

    async def __setup(self):
        await ACCIO.db.execute(
            "create table if not exists blockgroups (group_id integer unique)"
        )
        self.blockgroups = await self.get()
        self.__class__.instance = self

    @OnEvent[CQHTTPEvent].add_listener
    async def handle(self, evt: CQHTTPEvent):
        if group_id := getattr(evt, "group_id", None):
            if group_id in self.blockgroups:
                evt.cancel()

    async def get(self) -> set[int]:
        await ACCIO.db.execute("select group_id from blockgroups")
        result = await ACCIO.db.fatchall()
        return set(group[0] for group in result)

    async def add(self, group_id: int):
        blockgroups = self.blockgroups
        if group_id in blockgroups:
            log.warning("try to add group_id already exist")
            return
        await ACCIO.db.execute(
            "insert into blockgroups (group_id) values (?)", (group_id,)
        )
        blockgroups.add(group_id)

    async def delete(self, group_id: int):
        blockgroups = self.blockgroups
        if group_id not in blockgroups:
            log.warning("try to delete group_id not exist")
            return
        await ACCIO.db.execute(
            "delete from blockgroups where group_id = ?", (group_id,)
        )
        blockgroups.remove(group_id)