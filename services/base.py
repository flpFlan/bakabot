# -- stdlib --
import logging
from typing import Callable, Generic, Type, TypeVar, cast, get_args, get_type_hints
from re import compile

# -- third party --
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# -- own --
from accio import Accio
from cqhttp.base import Event

# -- code --

log = logging.getLogger("bot.service")

class ServiceBehavior:
    def __init__(self, service):
        self.service = cast(Service,service)
        self.set_active(False)

    def set_active(self, active: bool):
        self._active = active

    def get_active(self):
        return self._active

class Service:
    priority = 3
    behavior:list[Type[ServiceBehavior]] = []
    execute_before:list[Type[ServiceBehavior]] = []
    execute_after:list[Type[ServiceBehavior]] = []

    def __init__(self):
        self.set_active(False)

    def set_active(self,active:bool):
        self._active=active

    def get_active(self):
        return self._active

    async def start_up(self):
        db = Accio.bot.db
        service = self.__class__.__name__
        db.execute(
            """
            insert or replace into services (service,service_on) values (?,?)
            """,
            (service, True),
        )
        db.commit()
        for core in self.behavior:
            core.set_active(True)
        self.set_active(True)

    async def shutdown(self):
        db = bot.db
        service = self.__class__.__name__
        db.execute(
            "insert or replace into services (service,service_on) values (?,?)",
            (service, False),
        )
        db.commit()
        for core in self.behavior:
            core.set_active(False)
        self.set_active(False)

_TEvent=TypeVar("_TEvent",bound=Event)

class EventHandler(Generic[_TEvent]):
    handlers:dict[Event,set[Callable[[ServiceBehavior,_TEvent],_TEvent]]]
 
    @staticmethod
    def register(f:Callable[[ServiceBehavior,_TEvent],_TEvent]):
        args=list(get_type_hints(f).values())
        assert len(args)==1,"there must be one param with type declaration!"
        args=set(get_args(args[0]))
        from cqhttp.base import
        for arg in args:
            for evt in all_events:
                if not issubclass(evt,arg):
                    continue

        return f


class SheduledHandler(ServiceBehavior):
    shedule_trigger: str
    args: dict

    def run(self):
        super().run()
        self.jobs = jobs = []
        self.scheduler = scheduler = AsyncIOScheduler()
        if self.shedule_trigger == "interval":
            jobs.append(scheduler.add_job(self.handle, "interval", **self.args))
        if self.shedule_trigger == "cron":
            jobs.append(scheduler.add_job(self.handle, "cron", **self.args))
        scheduler.start()

    def close(self):
        super().close()
        self.scheduler.remove_all_jobs()
        self.jobs = []

    async def handle(self):
        ...

class IMessageFilter:
    from cqhttp.events.message import Message

    entrys = []
    entry_flags = 0

    def __init_subclass__(cls):
        entry=cls.entrys
        cls.entrys=[compile(et, cls.entry_flags) for et in entry]

    def filter(self, evt: Message):
        msg = evt.message
        for _entry in self.entrys:
            if match := _entry.match(msg):
                return match.groupdict()

def register_service_to(*bots):
    if "all" in bots or "ALL" in bots:
        bots = [Accio.bot.name]

    def register(cls):
        if Accio.bot.name in bots:
            Accio.bot.services.append(cls)
        return cls

    def except_for(*_bots):
        include = [b for b in bots if b not in _bots]
        return register_service_to(include)

    register.except_for = except_for
    return register
