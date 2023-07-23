# -- stdlib --
import logging

# -- own --
from services.base import OnEvent, ServiceBehavior, IMessageFilter, Service
from cqhttp.events.notice import GroupPoked
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_operation.SetGroupLeave import SetGroupLeave
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.whitelist")
whitelist: set[int] = set()


class WhiteList(Service):
    async def __setup(self):
        WhiteList.instance = self
        ACCIO.db.execute(
            "create table if not exists whitelist (group_id integer unique)"
        )

    def get(self) -> set[int]:
        ACCIO.db.execute("select group_id from whitelist")
        result = ACCIO.db.fatchall()
        return set(group[0] for group in result)

    def add(self, group_id: int):
        if group_id in whitelist:
            log.warning("try to add group_id already exist")
            return
        ACCIO.db.execute("insert into whitelist (group_id) values (?)", (group_id,))
        whitelist.add(group_id)

    def delete(self, group_id: int):
        if group_id not in whitelist:
            log.warning("try to delete group_id not exist")
            return
        ACCIO.db.execute("delete from whitelist where group_id = ?", (group_id,))
        whitelist.remove(group_id)


class Ping(ServiceBehavior[WhiteList], IMessageFilter):
    entrys = [
        r"^(?P<action>/ping)\s+(?P<bot>.+)",
        r"^(?P<action>/delete)\s+(?P<bot>.+)",
        r"^(?P<action>/leave)$",
    ]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if evt.user_id not in ACCIO.bot.Administrators:
            return
        if not (r := self.filter(evt)):
            return

        match r["action"]:
            case "/ping":
                if not r["bot"] == ACCIO.bot.name:
                    return
                self.service.add(evt.group_id)
                await SendGroupMsg(evt.group_id, "%s已在本群启用！" % ACCIO.bot.name).do()
            case "/delete":
                if not r["bot"] == ACCIO.bot.name:
                    return
                self.service.delete(evt.group_id)
            case "/leave":
                await SetGroupLeave(evt.group_id).do()


class BlockGroup(ServiceBehavior[WhiteList]):
    async def __setup(self):
        global whitelist
        self.whitelist = whitelist = self.service.get()

    @OnEvent[GroupMessage, GroupPoked].add_listener
    async def handle(self, evt: GroupMessage | GroupPoked):
        if evt.group_id not in self.whitelist:
            evt.cancel()
