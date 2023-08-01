# -- stdlib --
import os, base64, json
from binascii import hexlify
from Crypto.Cipher import AES

# -- third party --
import fake_useragent

# -- own --
from services.base import OnEvent, Service, ServiceBehavior, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.cqcode import Music
from utils.request import Request


# -- code --
class Encrypyed:
    """传入歌曲的ID，加密生成'params'、'encSecKey 返回"""

    def __init__(self):
        self.pub_key = "010001"
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.nonce = "0CoJUm6Qyw8W8jud"

    def create_secret_key(self, size):
        return hexlify(os.urandom(size))[:16].decode("utf-8")

    def aes_encrypt(self, text, key):
        iv = "0102030405060708"
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        result = encryptor.encrypt(text.encode("utf-8"))
        result_str = base64.b64encode(result).decode("utf-8")
        return result_str

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(
            int(hexlify(text.encode("utf-8")), 16), int(pubKey, 16), int(modulus, 16)
        )
        return format(rs, "x").zfill(256)

    def work(self, ids, br=128000):
        text = {"ids": [ids], "br": br, "csrf_token": ""}
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {"params": encText, "encSecKey": encSecKey}
        return data

    def search(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {"params": encText, "encSecKey": encSecKey}
        return data


class SearchSong(Service):
    name = "点歌"


class SearchSongCore(ServiceBehavior[SearchSong], IMessageFilter):
    entrys = [r"^点歌(?P<song>.+)$"]

    async def __setup(self):
        self.headers = {
            "User-Agent": fake_useragent.UserAgent().random,
            "Host": "music.163.com",
            "Referer": "http://music.163.com/search/",
        }
        self.ep = Encrypyed()

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            id = await self.search_song(r["song"])
            if id is None:
                await SendGroupMsg(evt.group_id, "啊哦Σ(⊙▽⊙，没有找到相关歌曲").do()
                return
            if id == "error":
                await SendGroupMsg(evt.group_id, "牙白，发生了不知名的错误！").do()
                return
            await SendGroupMsg(evt.group_id, Music("163", id)).do()

    async def search_song(self, search_content, search_type=1, limit=1):
        """
            根据音乐名搜索
        :params search_content: 音乐名
        :params search_type: 不知
        :params limit: 返回结果数量
        return: 可以得到id 再进去歌曲具体的url
        """
        url = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        text = {
            "s": search_content,
            "type": search_type,
            "offset": 0,
            "sub": "false",
            "limit": limit,
        }
        data = self.ep.search(text)
        result = await Request.post_json(url, data=data,headers=self.headers)
        if "result" not in result:
            return "error"
        elif "songCount" not in result["result"]:
            return None
        elif result["result"]["songCount"] <= 0:
            return None
        else:
            songs = result["result"]["songs"]
            for song in songs:
                song_id = song["id"]
                return song_id
