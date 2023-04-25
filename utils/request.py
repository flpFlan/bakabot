class Request:
    import requests
    from fake_useragent import UserAgent

    session = requests.Session()
    session.headers = {
        "User-agent": UserAgent().random,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
    }

    @classmethod
    def get(cls, url, *, headers=None, timeout=None):
        headers = headers or cls.session.headers
        return cls.session.get(url, headers=headers, timeout=timeout)

    @classmethod
    def post(cls, url, data=None, json=None, *, timeout=None, headers=None):
        headers = headers or cls.session.headers
        return cls.session.post(url, data, json, timeout=timeout, headers=headers)
