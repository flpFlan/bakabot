# -- stdlib --
import asyncio
import logging
import importlib
from inspect import ismodule

# -- third party --
# -- own --
from config import Administrators
from services.base import Service
from services.base import IMessageFilter, EventHandler
from .base import core_service
from cqhttp.events.message import Message, GroupMessage, PrivateMessage
from cqhttp.api.message.SendMsg import SendMsg
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --
log = logging.getLogger("bot.service.command")


def reload(*args):
    for arg in args:
        if ismodule(arg):
            importlib.reload(arg)
        else:
            importlib.reload(importlib.import_module(arg.__module__))


class CommandCore(EventHandler, IMessageFilter):
    interested = [Message]
    entrys = [
        # r"^/cmd\s+(?P<cmd>[\S]+)(?P<args>(?:\s+[\S]+)+)",
        r"^/cmd\s+(?P<cmd>[\s\S]+)",
    ]

    async def handle(self, evt: Message):
        qq = evt.user_id
        if not qq in Administrators:
            return
        if r := self.filter(evt):
            bot = self.bot
            commands = {"reload": reload}

            if isinstance(evt, GroupMessage):

                def sgm(msg, group_id=evt.group_id):
                    asyncio.ensure_future(
                        SendGroupMsg(group_id=group_id, message=msg).do(bot)
                    )

                def segm(msg, interval):
                    from services.core.whitelist import whitelist

                    SendGroupMsg.many(whitelist, msg).do(bot, interval)

            if isinstance(evt, PrivateMessage):

                def spm(msg, qq_number=evt.sender.user_id):
                    asyncio.ensure_future(
                        SendMsg(user_id=qq_number, message=msg).do(bot)
                    )

            cmd_raw = r["cmd"]
            try:
                # if cmd := commands.get(cmd_raw, None):
                #     cmd(*(eval(arg.strip()) for arg in r["args"].split()))
                # else:
                exec(cmd_raw)
            except Exception as e:
                log.error("error while excute command:\n%s", e)
                if isinstance(evt, GroupMessage):
                    await SendMsg(group_id=evt.group_id, message=str(e)).do(bot)

    async def close(self):
        log.warning("Command must be on")


class Catch(EventHandler, IMessageFilter):
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
        if self.filter(evt) is not None:
            self.catch = True


@core_service
class Command(Service):
    cores = [CommandCore, Catch]
