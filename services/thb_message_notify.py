# -- stdlib --
import argparse
import html
import re
from typing import cast

# -- third party --
from sqlalchemy import create_engine, text as sq_text
import redis

# -- own --
from services.base import register_to, Service, SheduledHandler
from cqhttp.api.message.SendGroupMsg import SendGroupMsg


# -- code --
thb_notify_groups = set()


class THBMessageNotifyCore(SheduledHandler):
    shedule_trigger = "interval"
    args = {"seconds": 5}

    def __init__(self, service):
        super().__init__(service)
        parser = argparse.ArgumentParser("forum_noti")
        parser.add_argument("--redis-url", default="redis://localhost:6379")
        parser.add_argument(
            "--connect-str", default="mysql://root@localhost/ultrax?charset=utf8"
        )
        parser.add_argument("--discuz-dbpre", default="pre_")
        parser.add_argument("--forums", default="2,36,38,40,78,82")
        parser.add_argument("--forums-thread-only", default="78")
        options = parser.parse_args()
        self.text = text = lambda t: sq_text(t.replace("cdb_", options.discuz_dbpre))

        self.engine = engine = create_engine(
            options.connect_str,
            encoding="utf-8",
            convert_unicode=True,
        )
        self.forum_ids = forum_ids = map(int, options.forums.split(","))
        forums = engine.execute(
            text(
                """
                SELECT fid, name FROM cdb_forum_forum
                WHERE fid IN :fids
                """
            ),
            fids=forum_ids,
        ).fetchall()
        self.forums = forums = {i.fid: i.name for i in forums}
        self.r = r = redis.from_url(options.redis_url)
        self.pid = int(r.get("aya:forum_lastpid") or 495985)
        self.post_template = "|G{user}|r在|G{forum}|r发表了新主题|G{subject}|r：{excerpt}"
        self.reply_template = "|G{user}|r回复了|G{forum}|r的主题|G{subject}|r：{excerpt}"
        self.threads_only = set(map(int, options.forums_thread_only.split(",")))

    async def handle(self):
        bot = self.bot
        service = cast(THBMessageNotify, self.service)

        engine = self.engine
        text = self.text
        pid = self.pid
        forum_ids = self.forum_ids
        r = self.r
        forums = self.forums
        threads_only = self.threads_only
        posts = engine.execute(
            text(
                """
            SELECT * FROM cdb_forum_post
            WHERE pid > :pid AND
                  fid IN :fids
            ORDER BY pid ASC
        """
            ),
            pid=pid,
            fids=forum_ids,
        )
        if not posts:
            return
        for p in posts:
            if not p.first and p.fid in threads_only:
                continue

            t = engine.execute(
                text(
                    """
                SELECT * FROM cdb_forum_thread
                WHERE tid = :tid
            """
                ),
                tid=p.tid,
            ).fetchone()

            template = self.post_template if p.first else self.reply_template

            excerpt = p.message.replace("\n", "")
            excerpt = html.unescape(excerpt)
            excerpt = re.sub(r"\[quote\].*?\[/quote\]", "", excerpt)
            excerpt = re.sub(r"\[img\].*?\[/img\]", "[图片]", excerpt)
            excerpt = re.sub(r"\[.+?\]", "", excerpt)
            excerpt = re.sub(r"\{:.+?:\}", "[表情]", excerpt)
            excerpt = re.sub(r" +", " ", excerpt)
            excerpt = excerpt.strip()
            if len(excerpt) > 60:
                excerpt = excerpt[:60] + "……"

            msg = template.format(
                user=p.author,
                forum=forums[t.fid],
                subject=t.subject,
                excerpt=excerpt,
            )
            pid = p.pid
            SendGroupMsg.many(service.thb_notify_groups, msg).do(bot)
        r.set("aya:forum_lastpid", pid)


# @register_to("ALL")
class THBMessageNotify(Service):
    cores = [THBMessageNotifyCore]

    async def start(self):
        from bot import Bot

        bot = cast(Bot, self.bot)
        bot.db.execute(
            "create table if not exists thb_notify_groups (group_id integer unique)"
        )
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
