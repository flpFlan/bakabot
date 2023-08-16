# -- stdlib --
import logging
from abc import ABC

# -- own --
from services.base import Service

# -- code --
log = logging.getLogger("bot.service.core_service")

class CoreService(Service, ABC):
    async def shutdown(self):
        log.warning(f"trying to shutdown core service: {self.__class__.__name__}")


# prevent this class from being instantiated
setattr(CoreService.shutdown, '__isabstractmethod__', True)
del CoreService.__abstractmethods__