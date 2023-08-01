# -- stdlib --
import os
from urllib.parse import urljoin
import requests

# -- own --
from services.base import Service, ServiceBehavior, OnEvent, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image
from accio import ACCIO

# -- code --
PID_PATH = ACCIO.conf.get("Service.Pid", "path")
PID_URL = ACCIO.conf.get("Service.Pid", "url")


class Pid(Service):
    name = "Pid"


class PidCore(ServiceBehavior[Pid], IMessageFilter):
    entrys = [r"^pid\s*(?P<pid>\d+(?:-\d+)?)$"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        pid = r["pid"]
        try:
            if evt.user_id in ACCIO.bot.Administrators:
                if path := await self.get_art(pid):
                    m = f"{Image(f'file:///{path}')}"
                else:
                    m = "這個作品可能已被刪除，或無法取得。\n該当作品は削除されたか、存在しない作品IDです。"
            else:
                m = await self.get_art_webVer(pid)
                m = m or "這個作品可能已被刪除，或無法取得。\n該当作品は削除されたか、存在しない作品IDです。"

        except requests.ConnectTimeout:
            m = "请求失败，请稍后再试"

        await SendGroupMsg(evt.group_id, m).do()

    async def get_art(self, pid):
        url = f"https://pixiv.cat/{pid}.jpg"
        r = await Request.get(url)
        format = r.headers["Content-Type"].split("/")[1]
        if format == "html; charset=utf-8":
            return 0
        path = f"src/temp/pid_temp.{format}"
        with open(path, "wb") as file:
            for i in r.iter_content():
                file.write(i)
            file.close()
        return os.path.abspath(path)

    async def get_art_webVer(self, pid):
        url = f"https://pixiv.cat/{pid}.jpg"
        r = await Request.get(url)
        format = r.headers["Content-Type"].split("/")[1]
        if format == "html; charset=utf-8":
            return 0
        path = os.path.join(PID_PATH, f"{pid}.{format}")
        with open(path, "wb") as file:
            for i in r.iter_content():
                file.write(i)
            file.close()
        return urljoin(PID_URL, f"{pid}.{format}")
