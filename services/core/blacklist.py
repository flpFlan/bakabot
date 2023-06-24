# -- stdlib --
import logging
from typing import cast

# -- third party --
# -- own --
from services.core.base import core_service
from services.base import EventHub, Service
from cqhttp.events.message import Message

# -- code --
log = logging.getLogger("bot.service.blacklist")
blacklist: set[int] = set()


class BlockUser(EventHub):
    interested = [Message]

    def run(self):
        super().run()
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

    def __init__(self, bot):
        super().__init__(bot)
        self.bot.db.execute(
            "create table if not exists blacklist (qq_number integer unique)"
        )

    def get(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select qq_number from blacklist")
        result = db.fatchall()
        db.commit()
        return set(group[0] for group in result)

    def add(self, qq_number: int):
        if qq_number in blacklist:
            log.warning("try to add group_id already exist")
            return
        bot = self.bot
        db = bot.db

        db.execute(
            f"insert into blacklist (qq_number) values (?)",
            (qq_number,),
        )
        db.commit()
        blacklist.add(qq_number)

    def delete(self, qq_number: int):
        if qq_number not in blacklist:
            log.warning("try to delete qq_number not exist")
            return
        bot = self.bot
        bot.db.execute("delete from blacklist where qq_number = ?", (qq_number,))
        blacklist.remove(qq_number)

    def shutdown(self):
        log.warning("core service could not be close")
