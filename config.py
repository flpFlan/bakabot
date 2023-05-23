Administrators = [2104357372, 1502300947]  # users who have full control of your bot

from bot import Bot

_Bot_: Bot = Bot("BAKA", 2104357372)  # Bot("Aya", 0)

Endpoint = {
    "event": "localhost:2333",
    "api": "localhost:2334",
}  # value should be same with that in go-cqhttp's config.yml
