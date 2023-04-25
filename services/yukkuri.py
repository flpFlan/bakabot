# -- stdlib --
import requests, os
from bs4 import BeautifulSoup
from urllib.parse import quote

# -- third party --
# -- own --
from services.base import register_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
type = {
    "1": "f1",
    "2": "f2",
    "3": "m1",
    "4": "m2",
    "5": "dvd",
    "6": "imd1",
    "7": "jgr",
    "8": "r1",
}


class YukkuriCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^油库里(?P<type>[1-8])?(?P<content>.+)"]

    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            bot = self.bot
            group_id = evt.group_id

            type = r.get("type") or "f1"
            content = r.get("content")
            try:
                content = self.trans_to_jp(content).replace(" ", "")
            except requests.ConnectTimeout:
                await SendGroupMsg(group_id, "反应不能(✘_✘)").do(bot)
                return

            if len(content) > 140:
                await SendGroupMsg(group_id, "超出字数限制").do(bot)
                return
            self.get_yukkuri(content, sub_type=type)
            path = os.path.abspath(r"src\temp\yukkuri_temp.mp3")
            await SendGroupMsg(group_id, f"[CQ:record,file=file:///{path}]").do(bot)

    def get_yukkuri(self, text, type=1, sub_type="f1"):
        text = quote(text)
        r = Request.get(
            f"https://www.yukumo.net/api/v2/aqtk{type}/koe.mp3?type={sub_type}&kanji={text}"
        )
        r.raise_for_status()
        with open(r".\src\temp\yukkuri_temp.mp3", "wb") as file:
            for i in r.iter_content(100000):
                file.write(i)
            file.close()

    def trans_to_jp(self, text):
        """把中文变为日语（读音相同）"""
        data = {
            "contents": f"{text}",
            "firstinput": "OK",
            "option": "1",
            "optionext": "zenkaku",
        }
        r = Request.post(
            "https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in"
            "-simplified-chinese.php",
            data=data,
        )
        r.raise_for_status()
        return self.filt_html(r.text)

    def filt_html(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        result = soup.find("div", class_="finalresult")
        result = result.find_all(text=True)  # type: ignore
        final_result = ""
        for i in result:
            if i.startswith("(") and i.endswith(")"):
                result.remove(i)
        for i in result:
            final_result += i
        return final_result


@register_to("ALL")
class Yukkuri(Service):
    cores = [YukkuriCore]
