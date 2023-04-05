# -- stdlib --
from typing import Type
from re import RegexFlag

# -- third party --
# -- own --
from bot import Bot
from config import Bots
from service import all_services

# -- code --


class Service:
    service_on = False
    category: tuple
    interested: tuple
    entry: list
    entry_flags: RegexFlag
    excute_before: list
    excute_after: list

    def __init__(self, bot: Bot):
        self.bot = bot

    async def process(self) -> bool:
        ...  # to override it

    def start(self):
        self.service_on = True

    def close(self):
        self.service_on = False


class GroupService(Service):
    ...


def register_to(*bots):
    if "all" or "ALL" in bots:
        bots = [b.name for b in Bots]

    def register(cls: Type[Service]):
        for b in Bots:
            if b.name in bots:
                b.services.append(cls(b))

    def except_for(*_bots):
        include = [b for b in bots if b not in _bots]
        return register_to(include)

    register.except_for = except_for
    return register
