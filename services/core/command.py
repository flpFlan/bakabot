# -- stdlib --
import asyncio
import logging
import importlib
from inspect import ismodule

# -- own --
from .base import CoreService
from services.base import IMessageFilter, ServiceBehavior, OnEvent
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


class Command(CoreService):
    pass


class CommandCore(ServiceBehavior[Command], IMessageFilter):
    entrys = [r"^/cmd\s+(?P<cmd>[\s\S]+)"]

    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        if not evt.user_id in ACCIO.bot.Administrators:
            return
        if not (r := self.filter(evt)):
            return

        env = {}

        def clear_group():
            async def clear():
                from cqhttp.api.group_info.GetGroupList import GetGroupList
                from cqhttp.api.group_operation.SetGroupLeave import SetGroupLeave
                from services.core.whitelist import whitelist

                l = await GetGroupList().do()
                for i in l["data"]:
                    if (group_id := i["data"]["group_id"]) not in whitelist:
                        await SetGroupLeave(group_id).do()

            asyncio.create_task(clear())

        env["clear_group"] = clear_group

        if isinstance(evt, GroupMessage):

            def sgm(msg, group_id=evt.group_id):
                SendGroupMsg(group_id=group_id, message=msg).forget()

            def segm(msg, interval):
                from services.core.whitelist import whitelist

                SendGroupMsg.many(whitelist, msg).interval(interval).forget()

            env["sgm"] = sgm
            env["segm"] = segm

        if isinstance(evt, PrivateMessage):

            def spm(msg, qq_number=evt.sender.user_id):
                SendMsg(user_id=qq_number, message=msg).forget()

            env["spm"] = spm

        cmd_raw = r["cmd"]
        try:
            if evt.user_id == ACCIO.bot.SUPERUSER:
                exec(cmd_raw)
            else:
                exec(cmd_raw, env)
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
