# -- stdlib --
import logging
from typing import cast

# -- third party --
# -- own --
from services.base import EventHandler, MessageHandler, Service
from services.core.base import core_service
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --
log = logging.getLogger("bot.service.whitelist")
whitelist: set[int] = set()


class BlockGroup(EventHandler):
    interested = [GroupMessage]

    def __init__(self, service):
        super().__init__(service)
        self.service = cast(WhiteList, self.service)
        service = self.service
        global whitelist
        self.whitelist = whitelist = service.get()

    async def handle(self, evt: GroupMessage):
        if evt.group_id not in self.whitelist:
            evt.cancel()


class Ping(MessageHandler):
    interested = [GroupMessage]
    entrys = [r"^(?P<ping>/ping)$", r"^(?P<delete>/delete)$"]

    async def handle(self, evt: GroupMessage):
        sender = evt.user_id

        from config import Administrators

        if sender not in Administrators:
            return

        if (r := self.fliter(evt)) is not None:
            bot = self.bot
            service = cast(WhiteList, self.service)
            id = evt.group_id
            if r.get("ping", None):
                service.add(id)
                await SendGroupMsg(id, "%s已在本群启用！" % bot.name).do(bot)
            if r.get("delete", None):
                service.delete(id)


@core_service
class WhiteList(Service):
    cores = [BlockGroup, Ping]

    def get(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select whitelist from %s" % (bot.name + "_core"))
        result = db.fatchall()
        db.commit()
        return set(group[0] for group in result)

    def add(self, group_id: int):
        if group_id in whitelist:
            log.warning("try to add group_id already exist")
            return
        bot = self.bot
        db = bot.db

        db.execute(
            "insert into %s (whitelist) values (?)" % (bot.name + "_core"), (group_id,)
        )
        db.commit()
        whitelist.add(group_id)

    def delete(self, group_id: int):
        if group_id not in whitelist:
            log.warning("try to delete group_id not exist")
            return
        bot = self.bot
        bot.db.execute(
            "delete from %s where whitelist = ?" % (bot.name + "_core"), (group_id,)
        )
        whitelist.remove(group_id)

    def close(self):
        log.warning("core service could not be close")
