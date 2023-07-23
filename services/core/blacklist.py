# -- stdlib --
import logging

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import Message
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.blacklist")
blacklist: set[int] = set()


class BlackList(Service):
    def __setup(self):
        ACCIO.db.execute(
            "create table if not exists blacklist (qq_number integer unique)"
        )

    def get(self) -> set[int]:
        db = ACCIO.db
        db.execute("select qq_number from blacklist")
        result = db.fatchall()
        db.commit()
        return set(group[0] for group in result)

    def add(self, qq_number: int):
        if qq_number in blacklist:
            log.warning("try to add group_id already exist")
            return
        db = ACCIO.db

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
        ACCIO.db.execute("delete from blacklist where qq_number = ?", (qq_number,))
        blacklist.remove(qq_number)


class BlockUser(ServiceBehavior[BlackList]):
    def __setup(self):
        global blacklist
        self.blacklist = blacklist = self.service.get()

    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        if evt.user_id in self.blacklist:
            evt.cancel()
