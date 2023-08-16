# -- stdlib --
import logging
from abc import ABC, abstractmethod

# -- own --
from services.base import Service

# -- code --
log = logging.getLogger("bot.service.core_service")

class CoreService(Service, ABC):
    
    @abstractmethod
    def _(self):
        """to make this class abstract, so that it won't be instantiated"""

    async def shutdown(self):
        log.warning(f"trying to shutdown core service: {self.__class__.__name__}")
