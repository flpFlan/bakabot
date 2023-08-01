# -- stdlib --
import json
import logging
import asyncio
from typing import cast

# -- third party --
import redis.asyncio as redis

# -- own --
from services.base import Service, ServiceBehavior
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from accio import ACCIO


# -- code --
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


class THBMessageNotify(Service):
    async def __setup(self):
        await ACCIO.db.execute(
            "create table if not exists thb_notify_groups (group_id integer unique)"
        )
        global thb_notify_groups
        self.thb_notify_groups = thb_notify_groups = await self.get_notify_group()

    async def get_notify_group(self) -> set[int]:
        await ACCIO.db.execute("select group_id from thb_notify_groups")
        result = await ACCIO.db.fatchall()
        return set(group[0] for group in result)

    async def add_notify_group(self, group_id: int):
        if group_id in self.thb_notify_groups:
            return

        await ACCIO.db.execute(
            f"insert into thb_notify_groups (group_id) values (?)",
            (group_id,),
        )
        self.thb_notify_groups.add(group_id)

    async def del_notify_group(self, group_id: int):
        if group_id not in self.thb_notify_groups:
            return
        await ACCIO.db.execute(
            "delete from thb_notify_groups where group_id = ?", (group_id,)
        )
        self.thb_notify_groups.remove(group_id)


class THBMessageNotifyCore(ServiceBehavior[THBMessageNotify]):
    async def __setup(self):
        url = ACCIO.conf.get("Service.THBMessageNotify", "url")
        self.sub = sub = redis.from_url(url).pubsub()
        await sub.psubscribe("thb.*")
        self.l = asyncio.create_task(self.loop())
        self.service.OnBeforeShutDown += self.on_shutdown

    async def on_shutdown(self):
        self.l.cancel()

    async def loop(self):
        try:
            async for msg in self.sub.listen():
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
            await asyncio.sleep(1)

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
        SendGroupMsg.many(service.thb_notify_groups, send).interval(1).forget()
