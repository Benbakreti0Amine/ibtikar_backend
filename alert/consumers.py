# alerts/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Join a group specific to the user
            await self.channel_layer.group_add(f"user_{self.user.id}", self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Remove the user from the group
            await self.channel_layer.group_discard(f"user_{self.user.id}", self.channel_name)

    # async def send_alert(self, event):
    #     # Send alert message to WebSocket
    #     message = event["message"]
    #     await self.send(text_data=json.dumps({"message": message}))
    async def send_alert(self, event):
            # Add the print statement for debugging
            print(f"Alert sent: {event['message']}")
            # Send the alert message to the WebSocket
            await self.send(text_data=json.dumps({"message": event["message"]}))
