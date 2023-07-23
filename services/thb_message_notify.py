# -- stdlib --
import json
import logging
import time
from typing import cast

# -- third party --
import redis

# -- own --
from services.base import Service, ServiceBehavior
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from accio import ACCIO


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


class THBMessageNotify(Service):
    async def __setup(self):
        ACCIO.db.execute(
            "create table if not exists thb_notify_groups (group_id integer unique)"
        )
        global thb_notify_groups
        self.thb_notify_groups = thb_notify_groups = self.get_notify_group()

    def get_notify_group(self) -> set[int]:
        ACCIO.db.execute("select group_id from thb_notify_groups")
        result = ACCIO.db.fatchall()
        return set(group[0] for group in result)

    def add_notify_group(self, group_id: int):
        if group_id in self.thb_notify_groups:
            return

        ACCIO.db.execute(
            f"insert into thb_notify_groups (group_id) values (?)",
            (group_id,),
        )
        self.thb_notify_groups.add(group_id)

    def del_notify_group(self, group_id: int):
        if group_id not in self.thb_notify_groups:
            return
        ACCIO.db.execute(
            "delete from thb_notify_groups where group_id = ?", (group_id,)
        )
        self.thb_notify_groups.remove(group_id)


# TODO
class THBMessageNotifyCore(ServiceBehavior[THBMessageNotify]):
    async def __setup(self):
        return
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
        SendGroupMsg.many(service.thb_notify_groups, send).forget(interval=1)

    def close(self):
        super().close()
        self.flag = True
