# -- stdlib --
import asyncio
import logging
import importlib
from inspect import ismodule

# -- own --
from services.base import Service
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import Message, GroupMessage, PrivateMessage
from cqhttp.api.message.SendMsg import SendMsg
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from accio import ACCIO

# -- code --
log = logging.getLogger("bot.service.command")


def reload(*args):
    for arg in args:
        if ismodule(arg):
            importlib.reload(arg)
        else:
            importlib.reload(importlib.import_module(arg.__module__))


class Command(Service):
    pass


class CommandCore(ServiceBehavior[Command], IMessageFilter):
    entrys = [r"^/cmd\s+(?P<cmd>[\s\S]+)"]

    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        if not evt.user_id in ACCIO.bot.Administrators:
            return
        if not (r := self.filter(evt)):
            return
        if isinstance(evt, GroupMessage):

            def sgm(msg, group_id=evt.group_id):
                asyncio.ensure_future(SendGroupMsg(group_id=group_id, message=msg).do())

            def segm(msg, interval):
                from services.core.whitelist import whitelist

                SendGroupMsg.many(whitelist, msg).interval(interval).forget()

        if isinstance(evt, PrivateMessage):

            def spm(msg, qq_number=evt.sender.user_id):
                asyncio.ensure_future(SendMsg(user_id=qq_number, message=msg).do())

        cmd_raw = r["cmd"]
        try:
            exec(cmd_raw)
        except Exception as e:
            log.error("error while excute command:\n%s", e)
            if isinstance(evt, GroupMessage):
                await SendMsg(group_id=evt.group_id, message=str(e)).do()


class Catch(ServiceBehavior[Command], IMessageFilter):
    entrys = [r"^.catch$"]
    catch = False

    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        if not evt.user_id in ACCIO.bot.Administrators:
            return
        if self.catch:
            globals()["rgs"] = evt.message
            self.catch = False
            return
        if self.filter(evt):
            self.catch = True
