# -- stdlib --
import logging
from typing import cast

# -- third party --
# -- own --
from services.base import EventHandler, IMessageFilter, Service
from services.core.base import core_service
from cqhttp.events.notice import GroupPoked
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_operation.SetGroupLeave import SetGroupLeave

# -- code --
log = logging.getLogger("bot.service.whitelist")
whitelist: set[int] = set()


class BlockGroup(EventHandler):
    interested = [GroupMessage, GroupPoked]

    def run(self):
        super().run()
        self.service = cast(WhiteList, self.service)
        service = self.service
        global whitelist
        self.whitelist = whitelist = service.get()

    async def handle(self, evt: GroupMessage | GroupPoked):
        if evt.group_id not in self.whitelist:
            evt.cancel()


class Ping(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [
        r"^(?P<ping>/ping)\s+(?P<bot>.+)",
        r"^(?P<delete>/delete)\s+(?P<bot>.+)",
        r"^(?P<leave>/leave)$",
    ]

    async def handle(self, evt: GroupMessage):
        sender = evt.user_id

        from config import Administrators

        if sender not in Administrators:
            return

        if (r := self.filter(evt)) is not None:
            bot = self.bot
            service = cast(WhiteList, self.service)
            id = evt.group_id
            if r.get("ping", None):
                name = r.get("bot", "")
                if not name == bot.name:
                    return
                service.add(id)
                await SendGroupMsg(id, "%s已在本群启用！" % bot.name).do()
            if r.get("delete", None):
                name = r.get("bot", "")
                if not name == bot.name:
                    return
                service.delete(id)
            if r.get("leave", None):
                await SetGroupLeave(evt.group_id).do()


@core_service
class WhiteList(Service):
    cores = [BlockGroup, Ping]

    def __init__(self, bot):
        super().__init__(bot)
        WhiteList.instance = self
        self.bot.db.execute(
            "create table if not exists whitelist (group_id integer unique)"
        )

    def get(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select group_id from whitelist")
        result = db.fatchall()
        db.commit()
        return set(group[0] for group in result)

    def add(self, group_id: int):
        if group_id in whitelist:
            log.warning("try to add group_id already exist")
            return
        bot = self.bot
        db = bot.db

        db.execute("insert into whitelist (group_id) values (?)", (group_id,))
        db.commit()
        whitelist.add(group_id)

    def delete(self, group_id: int):
        if group_id not in whitelist:
            log.warning("try to delete group_id not exist")
            return
        bot = self.bot
        bot.db.execute("delete from whitelist where group_id = ?", (group_id,))
        whitelist.remove(group_id)

    def shutdown(self):
        log.warning("core service could not be close")
