# -- stdlib --
import os
from urllib.parse import urljoin
import requests

# -- third party --
import aiohttp

# -- own --
from services.base import IMessageFilter, register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from options import PID_PATH, PID_URL

# -- code --


class PidCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^pid\s*(?P<pid>\d+(?:-\d+)?)$"]

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        pid = r.get("pid", "")
        try:
            from config import Administrators

            if evt.user_id in Administrators:
                if path := await self.get_art(pid):
                    m = f"[CQ:image,file=file:///{path}]"
                else:
                    m = "這個作品可能已被刪除，或無法取得。\n該当作品は削除されたか、存在しない作品IDです。"
            else:
                m = await self.get_art_webVer(pid)
                m = "" or "這個作品可能已被刪除，或無法取得。\n該当作品は削除されたか、存在しない作品IDです。"

        except requests.ConnectTimeout:
            m = "请求失败，请稍后再试"

        await SendGroupMsg(evt.group_id, m).do(self.bot)

    async def get_art(self, pid):
        url = f"https://pixiv.cat/{pid}.jpg"
        r = Request.Sync.get(url)
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
        r = Request.Sync.get(url)
        format = r.headers["Content-Type"].split("/")[1]
        if format == "html; charset=utf-8":
            return 0
        path = os.path.join(PID_PATH, f"{pid}.{format}")
        with open(path, "wb") as file:
            for i in r.iter_content():
                file.write(i)
            file.close()
        return urljoin(PID_URL, f"{pid}.{format}")


@register_to("ALL")
class Pid(Service):
    cores = [PidCore]
