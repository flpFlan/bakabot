# -- third party --
import asyncio
import json
import threading
from quart import websocket, Quart

# -- own --

# -- code --
app = Quart(__name__)
S = "赞助"


def change():
    global S
    while True:
        S = input("输入新的语句：")


threading.Thread(target=change).start()


@app.websocket("/event")
async def mock_event():
    while True:
        await websocket.send(
            json.dumps(
                {
                    "post_type": "message",
                    "message_type": "group",
                    "sub_type": "normal",
                    "message": S,
                }
            )
        )
        await asyncio.sleep(1)


@app.websocket("/api")
async def mock_api():
    while True:
        data = await websocket.receive()
        data = json.loads(data)
        print(data)
        await websocket.send(
            json.dumps(
                {
                    "status": "ok",
                    "retcode": 0,
                    "data": {"message_id": 1},
                }
            )
        )


if __name__ == "__main__":
    app.run("localhost", 2333)
