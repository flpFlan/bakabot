# -- stdlib --
import asyncio
import logging
import re
from typing import Optional, cast
import threading
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- third party --
# -- own --
from services.base import EventHandler, Service, IMessageFilter
from services.core.base import core_service
from cqhttp.events.base import CQHTTPEvent

# -- code --
log = logging.getLogger("bot.service.game")
all_games = {}


class GameBehavior(IMessageFilter):
    interested = []

    def __init__(self, bot, game):
        super().__init__()
        from bot import Bot

        self.bot = cast(Bot, bot)
        self.game = game

    async def handle(self, evt: CQHTTPEvent):
        ...

    async def _callback(self, arg):
        ...


class Game:
    behavior: list
    tick: int = 60

    def __init__(self, bot, group_id, owner_id):
        from bot import Bot

        self.bot = cast(Bot, bot)
        self.group_id = group_id
        self.owner_id = owner_id
        self.game_over = False
        self.behavior = [b(bot, self) for b in self.behavior]
        self.behavior = cast(list[GameBehavior], self.behavior)
        self.timer: Optional[threading.Timer] = None
        self.check()

    async def process_evt(self, evt: CQHTTPEvent):
        if self.game_over:
            return
        has_handler = False
        for b in self.behavior:
            if not any([True if isinstance(evt, i) else False for i in b.interested]):
                continue
            has_handler = True

            if r := (await b.handle(evt)):
                await b._callback(r)
            if self.game_over:
                if timer := self.timer:
                    timer.cancel()
                return

        if has_handler:
            self.check()

    def check(self):
        tick = self.tick
        if tick == -1:
            return
        if timer := self.timer:
            timer.cancel()

        def t():
            asyncio.run(
                SendGroupMsg(self.group_id, f"长时间未操作，游戏结束。({self.owner_id})").do(
                    self.bot
                )
            )
            self.kill()

        self.timer = timer = threading.Timer(tick, t)
        timer.start()

    def kill(self):
        self.game_over = True
        ManagerCore.games.remove(self)
        del self


class ManagerCore(EventHandler, IMessageFilter):
    interested = [CQHTTPEvent]
    entrys = [r"^/game\s+(?P<game>.+)"]
    games: list[Game] = []

    def __init__(self, service):
        super().__init__(service)
        self.game_graph = all_games

    async def handle(self, evt: CQHTTPEvent):
        from cqhttp.events.message import GroupMessage

        if isinstance(evt, GroupMessage):
            if r := self.filter(evt):
                game = r["game"]
                game = game.strip()
                if g := self.game_graph.get(game, None):
                    ManagerCore.games.append(g(self.bot, evt.group_id, evt.user_id))
                    return
        for game in ManagerCore.games:
            await game.process_evt(evt)


@core_service
class GameManager(Service):
    cores = [ManagerCore]

    def close(self):
        log.warning("core service could not be close")


def register_to_game(name: str):
    def register(cls):
        all_games[name] = cls
        return cls

    return register
