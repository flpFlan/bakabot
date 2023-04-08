# -- stdlib --
import logging

# -- third party --
# -- own --
from config import Administrators
from services.base import Service
from services.base import MessageHandler, register_to
from cqhttp.events.message import Message

# -- code --
log = logging.getLogger("bot.service")


class CommandCore(MessageHandler):
    interested = [Message]
    entrys = [r"(?<=^/cmd)(?:\s)*(?P<cmd>[\s\S]+)"]

    # async def handle(self, msg: Message):
    # ...

    async def handle(self, evt: Message):
        qq = evt.user_id
        if not qq in Administrators:
            return False
        try:
            cmd = self.fliter(evt)["cmd"]
            exec(cmd)
        except Exception as e:
            log.error("error while excute command:\n%s", e)
            return False
        return True

    async def close(self):
        log.warning("Command must be on")


@register_to("ALL")
class Command(Service):
    cores = [CommandCore]
