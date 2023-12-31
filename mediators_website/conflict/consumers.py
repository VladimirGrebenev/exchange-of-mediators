import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ConflictMessage, Conflict
from user.models import User, UserMessage, ContactUser
from channels.db import database_sync_to_async
from datetime import datetime
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Функция для Consumera чата конфликта
    """
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["user"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, sender, message_text, conflict):
        message = ConflictMessage(user=sender, message=message_text, conflict=conflict)
        message.save()

    @database_sync_to_async
    def get_conflict(self, room_name):
        return Conflict.objects.filter(id=room_name)[0]

    @database_sync_to_async
    def get_user(self, sender):
        return User.objects.filter(id=sender)[0]

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = self.scope['user'].id
        sender_user = self.scope['user']
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        conflict = await self.get_conflict(room_name=room_name)
        user_id = await self.get_user(sender=sender)
        message_time = timezone.now().strftime('%d %m %Y %H:%M')
        await self.save_message(sender=user_id, message_text=message, conflict=conflict)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                                   "message": message,
                                   "sender_firstname": sender_user.firstname,
                                   "sender_lastname": sender_user.lastname,
                                   "room_name": room_name,
                                   'message_time': message_time}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender_lastname = event["sender_lastname"]
        sender_firstname = event["sender_firstname"]
        room_name = event["room_name"]
        message_time = event['message_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              "sender_lastname": sender_lastname,
                                              "sender_firstname": sender_firstname,
                                              "room_name": room_name,
                                              'message_time': message_time}))


class ChatUserConsumer(AsyncWebsocketConsumer):
    """
    Функция для consumer общего чата
    """
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]  # Имя комнаты переданное из JS
        self.user = self.scope["user"]  # Пользователь который коннектится
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, sender, message_text, receive_user):
        message = UserMessage(from_user=sender, message=message_text, to_user=receive_user)
        message.save()

    @database_sync_to_async
    def save_contact(self, sender, receive_user, last_message_time):
        contact = ContactUser(user=receive_user, contact=sender, last_message_time=last_message_time, new_messages=True)
        contact.save()

    @database_sync_to_async
    def get_receive_user(self, to_user_id):
        return User.objects.filter(id=to_user_id)[0]

    @database_sync_to_async
    def get_sender(self, sender):
        return User.objects.filter(id=sender)[0]

    @database_sync_to_async
    def chek_contact(self, sender, receive_user):
        return ContactUser.objects.filter(user=receive_user, contact=sender)[0]

    @database_sync_to_async
    def update_contact(self, sender, receive_user, last_message_time, new_messages):
        ContactUser.objects.filter(user=sender,
                                   contact=receive_user).update(last_message_time=last_message_time,
                                                                new_messages=new_messages)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = self.scope['user'].id
        to_user_id = text_data_json["id_to_msg"]
        sender_user = self.scope['user']
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        to_user = await self.get_receive_user(to_user_id=to_user_id)
        sender = await self.get_sender(sender=sender_id)
        message_time_contact = timezone.now()
        message_time = timezone.now().strftime('%d %m %Y %H:%M')

        await self.save_message(sender=sender, message_text=message, receive_user=to_user)
        try:
            check_contact = await self.chek_contact(sender=sender, receive_user=to_user)
        except IndexError:
            await self.save_contact(sender=sender, receive_user=to_user, last_message_time=message_time_contact)
            print(f'contact saved')
        else:
            await self.update_contact(sender=sender,
                                      receive_user=to_user,
                                      last_message_time=message_time_contact,
                                      new_messages=False)
            await self.update_contact(sender=to_user,
                                      receive_user=sender,
                                      last_message_time=message_time_contact,
                                      new_messages=True)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                                   "message": message,
                                   "sender_firstname": sender_user.firstname,
                                   "sender_lastname": sender_user.lastname,
                                   "room_name": room_name,
                                   'message_time': message_time}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender_lastname = event["sender_lastname"]
        sender_firstname = event["sender_firstname"]
        room_name = event["room_name"]
        message_time = event['message_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              "sender_lastname": sender_lastname,
                                              "sender_firstname": sender_firstname,
                                              "room_name": room_name,
                                              'message_time': message_time}))
