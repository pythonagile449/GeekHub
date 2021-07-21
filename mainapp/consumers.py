import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TopMenuConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.hub = self.scope['url_route']['kwargs']['hub_name']

