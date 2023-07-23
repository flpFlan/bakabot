from typing import TypedDict


class CQHTTPEvent(TypedDict):
    post_type: str
    time: int
    self_id: int
