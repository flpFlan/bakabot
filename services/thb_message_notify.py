# -- stdlib --
import asyncio
import json
import logging
from threading import Thread
import time
from typing import cast

# -- third party --
import redis

# -- own --
from services.base import (
    register_to,
    Service,
    ServiceCore,
    EventHandler,
    IMessageFilter,
)
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.events.message import GroupMessage


# -- code --
URL = "redis://localhost:6379"

log = logging.getLogger("bot.service.thbMessage")
thb_notify_groups = set()


ServerNames = {
    b"forum": "论坛",
    b"localhost": "本机",
    b"lake": "雾之湖",
    b"forest": "魔法之森",
    b"hakurei": "博丽神社",
    b"aya": "文文专访",
}


class THBMessageNotifyCore(ServiceCore):
    shedule_trigger = "interval"
    args = {"seconds": 1}

    def run(self):
        super().run()

        self.sub = sub = redis.from_url(URL).pubsub()
        sub.psubscribe("thb.*")

        self.flag = False
        from threading import Thread

        self.thread = thread = Thread(target=self.loop, name="thb_message_notify")
        thread.start()

    def loop(self):
        while not self.flag:
            try:
                for msg in self.sub.listen():
                    if self.flag:
                        return
                    if msg["type"] not in ("message", "pmessage"):
                        continue

                    _, node, topic = msg["channel"].split(b".")[:3]
                    if not topic == b"speaker":
                        continue
                    message = json.loads(msg["data"])

                    self.on_message(node, message)
            except Exception as e:
                log.error(e)

            finally:
                time.sleep(1)

    def on_message(self, node, message):
        username, content = message

        import random, re

        foo = str(random.randint(0x10000000, 0xFFFFFFFF))
        content = content.replace("||", foo)
        content = re.sub(
            r"([\r\n]|\|(c[A-Fa-f0-9]{8}|s[12][A-Fa-f0-9]{8}|[BbIiUuHrRGYW]|LB|DB|![RGOB]))",
            "",
            content,
        )
        content = content.replace(foo, "||")

        send = "{}『文々。新闻』{}： {}".format(
            ServerNames.get(node, node),
            username,
            content,
        )
        service = cast(THBMessageNotify, self.service)
        bot = self.bot
        SendGroupMsg.many(service.thb_notify_groups, send).do(bot, interval=1)

    def close(self):
        super().close()
        self.flag = True


class NotifyGroupManager(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^/thb_message (?P<action>on|off)$"]

    async def handle(self, evt: GroupMessage):
        from config import Administrators

        if evt.user_id not in Administrators:
            return
        if r := self.filter(evt):
            action = r.get("action", None)
            bot = self.bot
            service = cast(THBMessageNotify, self.service)
            group_id = evt.group_id
            if action == "on":
                service.add_notify_group(group_id)
                await SendGroupMsg(group_id, "THBMessageNotify已启用").do(bot)
            if action == "off":
                service.del_notify_group(group_id)
                await SendGroupMsg(group_id, "THBMessageNotify已关闭").do(bot)


@register_to("Aya")
class THBMessageNotify(Service):
    cores = [NotifyGroupManager, THBMessageNotifyCore]

    async def start(self):
        await super().start()
        from bot import Bot

        bot = cast(Bot, self.bot)
        bot.db.execute(
            "create table if not exists thb_notify_groups (group_id integer unique)"
        )
        global thb_notify_groups
        self.thb_notify_groups = thb_notify_groups = self.get_notify_group()

    def get_notify_group(self) -> set[int]:
        bot = self.bot
        db = bot.db
        db.execute("select group_id from thb_notify_groups")
        result = db.fatchall()
        return set(group[0] for group in result)

    def add_notify_group(self, group_id: int):
        if group_id in self.thb_notify_groups:
            return
        bot = self.bot
        db = bot.db

        db.execute(
            f"insert into thb_notify_groups (group_id) values (?)",
            (group_id,),
        )
        self.thb_notify_groups.add(group_id)

    def del_notify_group(self, group_id: int):
        if group_id not in self.thb_notify_groups:
            return
        bot = self.bot
        bot.db.execute("delete from thb_notify_groups where group_id = ?", (group_id,))
        self.thb_notify_groups.remove(group_id)
