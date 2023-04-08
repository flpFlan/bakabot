from typing import Type


class ApiAction:
    class Response:
        status: str
        retcode: int
        msg: str | None = None
        wording: str | None = None
        data: object
        echo: str | None

    action: str
    echo: str


all_apis = []


def register_to_api(act: Type[ApiAction]):
    all_apis.append(act)
    return act
