# -- stdlib --
import asyncio

# -- third party --
import requests
from fake_useragent import UserAgent

# -- code --

HEADERS = {
    "User-agent": UserAgent().random,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
}


class Request:
    session = requests.session()
    session.headers = HEADERS

    @classmethod
    def get(cls, url, *, params=None, headers=None, timeout=None):
        return asyncio.to_thread(
            cls.session.get, url=url, params=params, headers=headers, timeout=timeout
        )

    @classmethod
    def post(cls, url, json, *, headers=None, timeout=None):
        return asyncio.to_thread(
            cls.session.post, url=url, json=json, headers=headers, timeout=timeout
        )

    @classmethod
    async def get_json(cls, url, *, params=None, headers=None, timeout=None) -> dict:
        r = await cls.get(url, params=params, headers=headers, timeout=timeout)
        return r.json()

    @classmethod
    async def get_text(cls, url, *, params=None, headers=None, timeout=None) -> str:
        r = await cls.get(url, params=params, headers=headers, timeout=timeout)
        return r.text

    @classmethod
    async def get_iter_content(cls, url, *, params=None, headers=None, timeout=None):
        r = await cls.get(url, params=params, headers=headers, timeout=timeout)
        return r.iter_content()

    @classmethod
    async def post_json(cls, url, *, data=None, headers=None, timeout=None) -> dict:
        r = await cls.post(url, json=data, headers=headers, timeout=timeout)
        return r.json()

    @classmethod
    async def post_text(cls, url, *, data=None, headers=None, timeout=None) -> str:
        r = await cls.post(url, json=data, headers=headers, timeout=timeout)
        return r.text
