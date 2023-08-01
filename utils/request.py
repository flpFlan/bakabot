# -- stdlib --
import asyncio

# -- third party --
import requests

# -- code --


class Request:

    @classmethod
    def get(cls, url, *, params=None, headers=None, timeout=None):
        return asyncio.to_thread(
            requests.get, url=url, params=params, headers=headers, timeout=timeout
        )

    @classmethod
    def post(cls, url, data, *, headers=None, timeout=None):
        return asyncio.to_thread(
            requests.post, url=url, data=data, headers=headers, timeout=timeout
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
        for c in r.iter_content():
            yield c

    @classmethod
    async def post_json(cls, url, *, data=None, headers=None, timeout=None) -> dict:
        r = await cls.post(url, data=data, headers=headers, timeout=timeout)
        return r.json()

    @classmethod
    async def post_text(cls, url, *, data=None, headers=None, timeout=None) -> str:
        r = await cls.post(url, data=data, headers=headers, timeout=timeout)
        return r.text
