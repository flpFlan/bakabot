# -- stdlib --
import logging
from typing import cast

# -- third party --
# -- own --
from services.core.base import core_service
from services.base import EventHandler, Service
from cqhttp.events.message import Message

# -- code --
log = logging.getLogger("bot.service.blacklist")
blacklist: set[int] = set()


class BlockUser(EventHandler):
    interested = [Message]

    def __init__(self, service):
        super().__init__(service)
        self.service = cast(BlackList, self.service)
        service = self.service
        global blacklist
        self.blacklist = blacklist = service.get()

    async def handle(self, evt: Message):
        if evt.user_id in self.blacklist:
            evt.cancel()


@core_service
class BlackList(Service):
    cores = [BlockUser]

    def get(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select blacklist from %s" % (bot.name + "_core"))
        result = db.fatchall()
        db.commit()
        return set(group[0] for group in result)

    def add(self, qq_number: int):
        if qq_number in blacklist:
            log.warning("try to add group_id already exist")
            return
        bot = self.bot
        db = bot.db
        table = bot.name + "_core"

        db.execute(
            f"insert into %s (blacklist) values (?)" % table,
            (qq_number,),
        )
        db.commit()
        blacklist.add(qq_number)

    def delete(self, qq_number: int):
        if qq_number not in blacklist:
            log.warning("try to delete group_id not exist")
            return
        bot = self.bot
        table = bot.name + "_core"
        bot.db.execute("delete from %s where blacklist = ?" % table, (qq_number,))
        blacklist.remove(qq_number)

    def close(self):
        log.warning("core service could not be close")
