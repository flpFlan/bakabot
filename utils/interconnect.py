# -- stdlib --
import json
import redis

# -- own --
from accio import ACCIO

# -- code --

class Interconnect:

    def __init__(self, url):
        self.pub = redis.from_url(url)
        self.sub = redis.from_url(url)

    def run(self):
        sub=self.sub.pubsub()
        sub.subscribe("bakabot.*")

        for msg in sub.listen():
            if msg['type'] not in ('message', 'pmessage'):
                continue
            
            _, bot_name, topic = msg['channel'].split('.')[:3]
            message = json.loads(msg['data'])

            self.on_message(bot_name, topic, message)

    def on_message(self, bot_name, topic, message):
        ...

    def publish(self,topic,data):
        self.pub.publish(f"bakabot.{ACCIO.bot.name}.{topic}",data)
        