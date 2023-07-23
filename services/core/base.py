# -- stdlib --
import logging

# -- own --
from services.base import Service
from cqhttp.base import Event

# -- code --
log = logging.getLogger("bot.service.core_service")


class CoreService(Service):
    async def handle(self, evt: Event) -> Event:
        ...  # to override it

    async def shutdown(self):
        log.warning(f"trying to shutdown core service: {self.__class__.__name__}")
