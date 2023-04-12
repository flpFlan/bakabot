# -- stdlib --
import logging

# -- third party --
# -- own --
from config import Administrators
from services.base import Service
from services.base import MessageHandler
from .base import core_service
from cqhttp.events.message import Message, GroupMessage
from cqhttp.api.message.SendMsg import SendMsg

# -- code --
log = logging.getLogger("bot.service.command")


class CommandCore(MessageHandler):
    interested = [Message]
    entrys = [r"^/cmd\s+(?P<cmd>[\s\S]+)"]

    async def handle(self, evt: Message):
        qq = evt.user_id
        if not qq in Administrators:
            return False
        command = {}
        if r := self.fliter(evt):
            cmd = r["cmd"]
            cmd = command.get(cmd, None) or cmd
            try:
                exec(cmd)
            except Exception as e:
                log.error("error while excute command:\n%s", e)
                if isinstance(evt, GroupMessage):
                    bot = self.bot
                    group_id = evt.group_id
                    await SendMsg(group_id=group_id, message=str(e)).do(bot)

    async def close(self):
        log.warning("Command must be on")


@core_service
class Command(Service):
    cores = [CommandCore]
