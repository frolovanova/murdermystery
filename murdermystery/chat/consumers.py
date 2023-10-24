import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

def read_waiting_room_state(game_code):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, 'staticfiles', 'chats', str(game_code), 'waiting_room_state.json')

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        # Handle the case when the file does not exist
        return None


from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        game_code = text_data_json['game_code']
        characterpair = text_data_json['characterpair']
        sender = text_data_json['sender']
        file_path = os.path.join('staticfiles', 'chats', game_code, f'{characterpair}.json')

        # Initialize an empty list if the file doesn't exist yet
        if not os.path.exists(file_path):
            chat_data = []
        else:
            # Load existing chat data from the file
            with open(file_path, 'r') as file:
                chat_data = json.load(file)

        # Append the new message to the chat data
        chat_data.append({
            'sender': sender,
            'message': message
        })

        # Save the updated chat data back to the file
        with open(file_path, 'w') as file:
            json.dump(chat_data, file)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'characterpair': characterpair,
                'sender': sender
            }
        )

    def chat_message(self, event):
        message = event['message']
        characterpair = event['characterpair']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'characterpair': characterpair,
            'sender': sender
        }))


from channels.generic.websocket import AsyncWebsocketConsumer
import json, os


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None

class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Add the client to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f'channel name {self.channel_name}')
        await self.accept()

        current_directory = os.getcwd()
        key =  self.room_name

        file_path = os.path.join(current_directory, 'staticfiles', 'chats', key,'waiting_room_state.json')    
        # Pass the 'key' variable to the template context}
        context = {'key': key }


        # Broadcast a message to the group when someone connects
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': context
            }
        )

    async def disconnect(self, close_code):
        # Remove the client from the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        print(event)
        print(type(event))
        key  = event['message']['key']
        event = read_waiting_room_state(key)
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event  # Send the JSON string
        }))

    async def connected(self, event):
        # Receive a broadcasted connected message
        message = event['message']
        print("Made ti herer")

        # Send the connected message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'message': message
        }))

        
from channels.generic.websocket import AsyncWebsocketConsumer
import json

import os
import json

def update_game_state(game_code, character, act, task_number, completed):
    try:
        # Define the file path
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, 'staticfiles', 'chats', game_code, 'task.json')

        # Check if the directory structure exists, create if not
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Load existing JSON or create a new one
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                game_state = json.load(json_file)
        else:
            game_state = {}

        # Create a nested dictionary for the character if it doesn't exist
        if character not in game_state:
            game_state[character] = {}

        # Create a nested dictionary for the act if it doesn't exist
        if act not in game_state[character]:
            game_state[character][act] = {}

        # Update the task status
        game_state[character][f"act{str(act)}"][int(task_number)-1] = completed

        # Save the updated JSON back to the file
        with open(file_path, 'w') as json_file:
            json.dump(game_state, json_file, indent=4)

        return True  # Success
    except Exception as e:
        print(f"Error updating game state: {str(e)}")
        return False  # Error

# Example usage:
# update_game_state("IBJ7C", "victoriavickyhart", "act1", 1, 1)


class GameMaster(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        print(f'websocket room is {self.room_name}')
        
        # Add the client to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f'channel name {self.channel_name}')
        
        await self.accept()

        current_directory = os.getcwd()
        key = self.room_name

        file_path = os.path.join(current_directory, 'staticfiles', 'chats', key, 'game_state.json')    
        
        # Pass the 'key' variable to the template context
        context = read_json_file(file_path)

        # Broadcast a message to the group when someone connects
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': context
            }
        )

    async def chat_message(self, event):
        message = event['message']
        characterpair  = event['characterpair']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    async def receive(self, text_data):
        print("heeeerreee")
        message = json.loads(text_data)
        command = message.get('command')

        if command == 'refresh':
            # Broadcast a message to all connected clients
            await self.send(text_data=json.dumps({'refresh': True}))
# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .views import get_act

class TaskWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        game_code = data.get('game_code')
        character = data.get('character')
        task = data.get('task')
        act = get_act(game_code)
        print(data)
        update_game_state(game_code, character, act, task, 1)

        # Handle the WebSocket message as before
        await self.send(text_data=json.dumps({
            'task': task,
            'completed_by': character,
        }))

from channels.generic.http import AsyncHttpConsumer
import json

class TaskHttpConsumer(AsyncHttpConsumer):
    async def http_request(self, message):
        # Handle the HTTP POST request here
        content_length = message.headers.get("content-length")
        body = await message.content.read(int(content_length))
        data = json.loads(body.decode('utf-8'))

        game_code = data.get('game_code')
        character = data.get('character')
        task = data.get('task')

        # Handle the task update and response for HTTP request
        # Update the JSON file or database to track completed tasks for characters
        # You can send an HTTP response to acknowledge the request
        await self.send_response(
            200,
            "OK",
            content_type="application/json",
            body=json.dumps({"message": "Task updated successfully"}),
        )