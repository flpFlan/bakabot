# -- stdlib --
import logging
from abc import ABC

# -- own --
from services.base import Service

# -- code --
log = logging.getLogger("bot.service.core_service")

#TODO: 此基类会实例化
class CoreService(Service, ABC):
    async def shutdown(self):
        log.warning(f"trying to shutdown core service: {self.__class__.__name__}")
