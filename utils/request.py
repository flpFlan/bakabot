# -- stdlib --
import requests

# -- third party --
from aiohttp import ClientSession
from fake_useragent import UserAgent

# -- own --
# -- code --

HEADERS = {
    "User-agent": UserAgent().random,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
}


class Request:
    class Sync:
        session = requests.session()
        session.headers = HEADERS

        @classmethod
        def get(cls, url, *, headers=None, timeout=None):
            return cls.session.get(url, headers=headers, timeout=timeout)

        @classmethod
        def post(cls, url, json, *, headers=None, timeout=None):
            return cls.session.post(url, json=json, headers=headers, timeout=timeout)

        @classmethod
        def get_json(cls, url, *, headers=None, timeout=None) -> dict:
            return cls.session.get(url, headers=headers, timeout=timeout).json()

        @classmethod
        def get_text(cls, url, *, headers=None, timeout=None) -> str:
            return cls.session.get(url, headers=headers, timeout=timeout).text

        @classmethod
        def get_iter_content(cls, url, *, headers=None, timeout=None):
            return cls.session.get(url, headers=headers, timeout=timeout).iter_content()

    @classmethod
    async def get_json(cls, url, *, headers=None, timeout=None) -> dict:
        headers = headers or HEADERS
        async with ClientSession(headers=headers, trust_env=True) as session:
            async with session.get(url, headers=headers, timeout=timeout) as r:
                return await r.json(content_type=r.content_type)

    @classmethod
    async def get_text(cls, url, *, headers=None, timeout=None) -> str:
        headers = headers or HEADERS
        async with ClientSession(headers=headers, trust_env=True) as session:
            async with session.get(url, headers=headers, timeout=timeout) as r:
                return await r.text()

    @classmethod
    async def get_iter_content(cls, url, *, headers=None, timeout=None):
        headers = headers or HEADERS
        async with ClientSession(headers=headers, trust_env=True) as session:
            async with session.get(url, headers=headers, timeout=timeout) as r:
                while chuck := r.content.read(1024):
                    yield chuck
