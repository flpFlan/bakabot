# -- stdlib --
from abc import abstractmethod, ABC
from collections import defaultdict
import logging
from typing import ClassVar, Generic, Type, TypeVar, get_args
import datetime
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- own --
from services.base import OnEvent, Service, IMessageFilter, ServiceBehavior
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage
from utils.wrapper import Scheduled
from utils import chronos

# -- code --
log = logging.getLogger("bot.service.game")
all_games: dict[str, "Game"] = {}


class Game:
    behaviors: ClassVar[list[Type["GameBehavior"]]]
    tick: float = 60

    def __init__(self, group_id, owner_id):
        self.group_id = group_id
        self.owner_id = owner_id
        self.game_over = False
        self._behavior = [bhv(self) for bhv in self.__class__.behaviors]

        async def t():
            if not self.game_over:
                await SendGroupMsg(self.group_id, f"长时间未操作，游戏结束。({self.owner_id})").do()
            self.kill()

        with Scheduled.Date(forget=True) as schedule:
            now = datetime.datetime.now()
            delta = datetime.timedelta(seconds=self.tick)
            self._killer_job = schedule.run_date(now + delta).add(t)

    async def __setup(self):
        ...  # to override it

    async def process_evt(self, evt: CQHTTPEvent):
        if self.game_over:
            return
        has_handler = False
        for b in self._behavior:
            if not any(filter(lambda x: isinstance(evt, x), b.interested)): # type: ignore
                continue
            if not b.check(evt):
                continue
            has_handler = True

            if r := (await b.handle(evt)):
                await b._callback(r)
            if self.game_over:
                if job := self._killer_job:
                    job.remove()
                return

        if has_handler:
            self.reset_clock()

    def reset_clock(self):
        if self.tick == -1:
            return
        if job := self._killer_job:
            now = datetime.datetime.now()
            delta = datetime.timedelta(seconds=self.tick)
            job.modify(next_run_time=now + delta)

    def kill(self):
        self.game_over = True
        try:
            ManagerCore.games[self.group_id].pop(self.owner_id)
        except:
            pass

    @classmethod
    async def create_instance(cls, group_id, owner_id):
        self = cls(group_id, owner_id)
        if __setup := getattr(self, f"_{self.__class__.__name__}__setup", None):
            await __setup()
        return self


TGame = TypeVar("TGame", bound=Game)
TCQHTTPEvent = TypeVar("TCQHTTPEvent", bound=CQHTTPEvent)


class GameBehavior(Generic[TGame,TCQHTTPEvent], IMessageFilter, ABC):
    interested: ClassVar[tuple[Type[CQHTTPEvent],...]]

    def __init_subclass__(cls):
        type_args = get_args(getattr(cls,"__orig_bases__")[0])
        cls.interested = get_args(type_args[1])
        game_t = type_args[0]
        assert not hasattr(game_t, "__args__")  # cann't be union
        assert issubclass(game_t, Game)
        if not vars(game_t).get("behaviors"):
            game_t.behaviors = []
        if not cls in game_t.behaviors:
            game_t.behaviors.append(cls)

    def __init__(self, game: TGame):
        self.game = game
    
    @abstractmethod
    def check(self, evt: TCQHTTPEvent) -> bool:
        ...  # to override it

    @abstractmethod
    async def handle(self, evt: TCQHTTPEvent):
        ...

    async def _callback(self, arg):
        pass


class GameManager(Service):
    doc = "格式: /game <game>，具体请参考https://github.com/flpFlan/bakabot"


class ManagerCore(ServiceBehavior[GameManager], IMessageFilter):
    entrys = [r"^/game\s+(?P<game>.+)"]
    games: dict[int, dict[int, Game]] = defaultdict(dict)

    async def __setup(self):
        self.game_graph = all_games

    @OnEvent[CQHTTPEvent].add_listener
    async def handle(self, evt: CQHTTPEvent):
        if isinstance(evt, GroupMessage):
            if r := self.filter(evt):
                group_id, user_id, game = evt.group_id, evt.user_id, r["game"].strip()
                if g := self.game_graph.get(game, None):
                    if i := ManagerCore.games[group_id].get(user_id, None):
                        i.kill()
                    ManagerCore.games[group_id][user_id] = await g.create_instance(
                        group_id, user_id
                    )
                    return
        for group_id in ManagerCore.games:
            for game in [
                *ManagerCore.games[group_id].values()
            ]:  # NOTE: 防止迭代过程中games被修改
                await game.process_evt(evt)


def register_to_game(name: str):
    def register(cls):
        all_games[name] = cls
        return cls

    return register
