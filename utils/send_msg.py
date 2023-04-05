# -- stdlib --
import requests
import time
from typing import Mapping, Literal
import logging

# -- third party --
# -- own --
from config import POST_PORT

# -- code --
MAX_RETRIES = 1
URL = f"http://127.0.0.1:{POST_PORT}/send_msg"

log = logging.getLogger("Bot_SMG")


def send_msg(resp_dict, auto_escape=False, ignore=False) -> int:
    msg_type: str = resp_dict["msg_type"]
    number: int = resp_dict["number"]
    msg: str = resp_dict["msg"]

    if not (msg_type and number and msg):
        log.error("SMG::missing parameter")
        return 0

    if msg_type == "group":
        data = {
            "message_type": "group",
            "group_id": number,
            "message": msg,
            "auto_escape": auto_escape,
        }

    elif msg_type == "private":
        data = {
            "message_type": "private",
            "user_id": number,
            "message": msg,
            "auto_escape": auto_escape,
        }

    else:
        data = {}
        log.warning("SMG::Empty Data")

    try:
        success = False
        current_retry = 0

        while current_retry <= MAX_RETRIES:
            log.debug("发送:%s", data)
            r = requests.post(URL, json=data).json()
            if isinstance(r, int):
                success = True
                break
            current_retry += 1

        if not success:
            if r["status"] == "failed" and not ignore:
                time.sleep(1)
                r = send_msg(
                    {"msg_type": msg_type, "number": number, "msg": "谔谔，该消息被腾讯拦截"},
                    ignore=True,
                )
            else:
                return 0
        return r
    except Exception as e:
        log.exception(e)
        return 0
