# -- stdlib --
from ast import While
import asyncio
import logging

# -- third party --
# -- own --
from config import Administrators
from services.base import Service
from services.base import IMessageFliter, EventHandler
from .base import core_service
from cqhttp.events.message import Message, GroupMessage, PrivateMessage
from cqhttp.api.message.SendMsg import SendMsg
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --
log = logging.getLogger("bot.service.command")


class CommandCore(EventHandler, IMessageFliter):
    interested = [Message]
    entrys = [r"^/cmd\s+(?P<cmd>[\s\S]+)"]

    async def handle(self, evt: Message):
        qq = evt.user_id
        if not qq in Administrators:
            return
        if r := self.fliter(evt):
            bot = self.bot
            commands = {}

            if isinstance(evt, GroupMessage):

                def sgm(msg, group_id=evt.group_id):
                    asyncio.run(SendGroupMsg(group_id=group_id, message=msg).do(bot))

                def segm(msg, interval):
                    from services.core.whitelist import whitelist

                    SendGroupMsg.many(whitelist, msg).do(bot, interval)

            if isinstance(evt, PrivateMessage):

                def spm(msg, qq_number=evt.sender.user_id):
                    asyncio.run(SendMsg(user_id=qq_number, message=msg).do(bot))

            cmd = r["cmd"]
            cmd = commands.get(cmd, None) or cmd
            try:
                exec(cmd)
            except Exception as e:
                log.error("error while excute command:\n%s", e)
                if isinstance(evt, GroupMessage):
                    await SendMsg(group_id=evt.group_id, message=str(e)).do(bot)

    async def close(self):
        log.warning("Command must be on")


class Catch(EventHandler, IMessageFliter):
    interested = [GroupMessage]
    entrys = [r"^.catch$"]
    catch = False

    async def handle(self, evt: GroupMessage):
        if not evt.user_id in Administrators:
            return
        if self.catch:
            globals()["rgs"] = evt.message
            self.catch = False
            return
        if self.fliter(evt) is not None:
            self.catch = True


@core_service
class Command(Service):
    cores = [CommandCore, Catch]
