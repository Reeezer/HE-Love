# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, AppUser, Match
from django.db.models import Q
import threading

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        message = text_data_json['message']
        date_time = text_data_json['date_time']
        insertion = text_data_json['insertion']
        
        ##Insert in DB HERE
        t = threading.Thread(target=database_chat_insertion,args=[insertion])
        t.setDaemon(True)
        t.start()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender' : sender,
                'message': message,
                'date_time': date_time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']
        date_time = event['date_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message,
            'date_time': date_time
        }))
        
       ## Database insertion
def database_chat_insertion(insertion):
    insertion = insertion.split('|')
    f = open("log.txt","w")
    f.write(f"insertion 0 : {insertion[0]}\n")
    f.write(f"insertion 1 : {insertion[1]}\n")
    f.write(f"insertion 2 : {insertion[2]}\n")
    f.write(f"insertion 3 : {insertion[3]}\n")
    f.write(f"insertion 4 : {insertion[4]}\n")
    
    get_sender = AppUser.objects.get(username=insertion[0])
    f.write(f"get_sender : {get_sender}\n")
    get_receiver = AppUser.objects.get(username=insertion[1])
    f.write(f"get_receiver : {get_sender}\n")
    get_message = insertion[2]
    f.write(f"get_message : {get_message}\n")
    get_date = insertion[3]
    f.write(f"get_date : {get_date}\n")
    get_match = Match.objects.get(pk=insertion[4])
    f.write(f"get_match : {get_match}\n")
    
    value_to_insert = Chat(user_sender=get_sender,
                            user_receiver=get_receiver,
                            message=insertion[2],
                            date=get_date,
                            match=get_match)
    
    value_to_insert.save()