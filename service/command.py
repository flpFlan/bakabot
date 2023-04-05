# -- stdlib --
import logging
from typing import Mapping

# -- third party --
# -- own --
from service import log
from service.base import Service, register_to
from config import Administrators

# -- code --


@register_to("ALL")
class Command(Service):
    category = ("message",)
    interested = ("private", "group")
    entry = [r"(?<=^/cmd)(?:\s)*(?P<cmd>[\s\S]+)"]

    async def process(self, qq: int, cmd: str) -> bool:
        if not qq in Administrators:
            return False
        try:
            exec(cmd)
        except Exception as e:
            log.error("error while excute command:\n%s", e)
            return False
        return True

    def close(self):
        log.warning("Command must be on")
