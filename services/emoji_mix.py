# -- stdlib --
import re

# -- third party --
import emoji

# -- own --
from services.base import IMessageFilter, register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request


# -- code --
emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
pattern = "(" + "|".join(re.escape(u) for u in emojis) + ")"


class EmojiError(Exception):
    pass


class EmojiMixCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [rf"^emoji合成\s*(?P<emoji>{pattern}{{2}})$"]

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        emoji1 = r.get("emoji", "")[0]
        emoji2 = r.get("emoji", "")[1]
        self.format_emoji(emoji1)
        self.format_emoji(emoji2)
        try:
            url = self.get_mix_url(emoji1, emoji2)
            m = f"[CQ:image,file={url}]"
        except EmojiError:
            m = '啊哦，似乎发生了一些错误Σ(⊙▽⊙"a\n请检查内容后重试'

        await SendGroupMsg(evt.group_id, m).do(self.bot)

    def get_mix_url(self, emoji1, emoji2):
        emoji1 = hex(ord(emoji1)).replace("0x", "u")
        emoji2 = hex(ord(emoji2)).replace("0x", "u")

        for _ in range(2):
            url = f"https://www.gstatic.com/android/keyboard/emojikitchen/20201001/{emoji1}/{emoji1}_{emoji2}.png"
            if Request.get(url).ok:
                return url
            emoji1, emoji2 = emoji2, emoji1

        raise EmojiError()

    def format_emoji(self, emoji: str):
        if "️" in emoji:
            emoji = emoji.replace("️", "") + "-ufe0f"
        return emoji


@register_to("ALL")
class EmojiMix(Service):
    cores = [EmojiMixCore]
