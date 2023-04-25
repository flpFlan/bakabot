# -- stdlib --
import logging
from typing import cast

# -- third party --
# -- own --
from services.core.base import core_service
from services.base import EventHandler, Service, IMessageFilter
from cqhttp.base import Event
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --
log = logging.getLogger("bot.service.coreManager")


class BlockGroup(EventHandler):
    interested = [Event]

    def run(self):
        super().run()
        db = self.bot.db
        db.execute("create table if not exists blockgroups (group_id integer unique)")
        self.blockgroups = self.get()
        BlockGroup.instance = self

    async def handle(self, evt: Event):
        if group_id := getattr(evt, "group_id", None):
            if group_id in self.blockgroups:
                if isinstance(evt, SendGroupMsg):
                    if evt._.args.get("bot off", None):
                        return
                evt.cancel()

    def get(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select group_id from blockgroups")
        result = db.fatchall()
        return set(group[0] for group in result)

    def add(self, group_id: int):
        blockgroups = self.blockgroups
        if group_id in blockgroups:
            log.warning("try to add group_id already exist")
            return
        bot = self.bot
        db = bot.db

        db.execute("insert into blockgroups (group_id) values (?)", (group_id,))
        db.commit()
        blockgroups.add(group_id)

    def delete(self, group_id: int):
        blockgroups = self.blockgroups
        if group_id not in blockgroups:
            log.warning("try to delete group_id not exist")
            return
        bot = self.bot
        bot.db.execute("delete from blockgroups where group_id = ?", (group_id,))
        blockgroups.remove(group_id)

    def close(self):
        pass


class BotControl(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^/bot on$", r"^/bot off$"]

    async def handle(self, evt: GroupMessage):
        from config import Administrators

        if not (evt.sender.role in ("owner", "admin") or evt.user_id in Administrators):
            return
        bot = self.bot
        msg = evt.message
        group_id = evt.group_id
        if msg == "/bot on":
            BlockGroup.instance.delete(group_id)
            await SendGroupMsg(group_id, f"{bot.name} running！").do(bot)
        if msg == "/bot off":
            BlockGroup.instance.add(group_id)
            c = SendGroupMsg(group_id, f"{bot.name} closed")
            c._.args["bot off"] = True
            await c.do(bot)

    def close(self):
        pass


class ServiceControl(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [
        r"^/(?P<get>get)$",
        r"/close (?P<service_to_close>.+)",
        r"/start (?P<service_to_start>.+)",
    ]

    async def handle(self, evt: GroupMessage):
        from config import Administrators

        if not evt.user_id in Administrators:
            return
        if r := self.filter(evt):
            group_id = evt.group_id
            if r.get("get", None):
                bot = self.bot
                await SendGroupMsg(group_id, str(self.get_all_services())).do(bot)
            if s := r.get("service_to_close", None):
                await self.close_service(group_id, s)
            if s := r.get("service_to_start", None):
                await self.start_service(group_id, s)

    def get_all_services(self):
        bot = self.bot
        graph = {
            service.__class__.__name__: service.service_on for service in bot.services
        }
        return graph

    async def close_service(self, group_id, service):
        bot = self.bot
        for s in bot.services:
            if s.__class__.__name__ == service:
                if not s.service_on:
                    await SendGroupMsg(group_id, f"{service}已处于关闭状态！").do(bot)
                    return
                await s.close()
                await SendGroupMsg(group_id, f"{service}已关闭").do(bot)

    async def start_service(self, group_id, service):
        bot = self.bot
        for s in bot.services:
            if s.__class__.__name__ == service:
                if s.service_on:
                    await SendGroupMsg(group_id, f"{service}已处于开启状态！").do(bot)
                    return
                await s.start()
                await SendGroupMsg(group_id, f"{service}已开启").do(bot)

    def close(self):
        pass


@core_service
class CoreManager(Service):
    cores = [BlockGroup, BotControl, ServiceControl]
