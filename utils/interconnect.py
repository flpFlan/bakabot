# -- stdlib --
import json

# -- own --
from accio import ACCIO

# -- third party --
import redis.asyncio as redis

# -- code --

class Interconnect:

    def __init__(self, url):
        self.pub = redis.from_url(url)
        self.sub = redis.from_url(url)

    async def run(self):
        sub=self.sub.pubsub()
        await sub.subscribe("bakabot.*")

        async for msg in sub.listen():
            if msg['type'] not in ('message', 'pmessage'):
                continue
            
            _, bot_name, topic = msg['channel'].split('.')[:3]
            message = json.loads(msg['data'])

            await self.on_message(bot_name, topic, message)

    async def on_message(self, bot_name, topic, message):
        ...

    async def publish(self,topic,data):
        await self.pub.publish(f"bakabot.{ACCIO.bot.name}.{topic}",data)
        