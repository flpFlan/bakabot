# -- stdlib --
import requests, os
from bs4 import BeautifulSoup
from urllib.parse import quote

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Record

# -- code --
TYPE = {
    "1": "f1",
    "2": "f2",
    "3": "m1",
    "4": "m2",
    "5": "dvd",
    "6": "imd1",
    "7": "jgr",
    "8": "r1",
}


class Yukkuri(Service):
    """食用方法：油库里 + 1-8(可选，表示音源种类) + 文本"""

    name = "油库里"


class YukkuriCore(ServiceBehavior[Yukkuri], IMessageFilter):
    entrys = [r"^油库里(?P<type>[1-8])?(?P<content>.+)"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            group_id = evt.group_id

            type, content = r["type"] or "f1", r["content"]
            try:
                content = (await self.trans_to_jp(content)).replace(" ", "")
            except requests.ConnectTimeout:
                await SendGroupMsg(group_id, "反应不能(✘_✘)").do()
                return

            if len(content) > 140:
                await SendGroupMsg(group_id, "超出字数限制").do()
                return
            await self.get_yukkuri(content, sub_type=TYPE.get(type, "") or type)
            path = os.path.abspath(r"src\temp\yukkuri_temp.mp3")
            await SendGroupMsg(group_id, Record(f"file:///{path}")).do()

    async def get_yukkuri(self, text, type=1, sub_type="f1"):
        text = quote(text)
        url = f"https://www.yukumo.net/api/v2/aqtk{type}/koe.mp3?type={sub_type}&kanji={text}"
        with open(r".\src\temp\yukkuri_temp.mp3", "wb") as file:
            for i in await Request.get_iter_content(url):
                file.write(i)
            file.close()

    async def trans_to_jp(self, text):
        """把中文变为日语（读音相同）"""
        data = {
            "contents": f"{text}",
            "firstinput": "OK",
            "option": "1",
            "optionext": "zenkaku",
        }
        url = "https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php"
        r = await Request.post_text(url, data=data)
        return self.filt_html(r)

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
