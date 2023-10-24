from django.shortcuts import render, redirect
import os
from django.urls import reverse
import random
import string

import os
import json

import os
import json

def initialize_game_state(game_code):
    try:
        # Define the file path
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, 'staticfiles', 'chats', game_code, 'task.json')

        # Check if the file already exists
        if not os.path.exists(file_path):
            # Create the directory structure if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Define the initial game state data
            game_state_data = {
                "detectivejohnson": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                },
                "mselizabethblackwood": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                },
                "professorarthurgrayson": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                },
                "victoriavickyhart": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                },
                "drjonathansmith": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                },
                "emilyjohnson": {
                    "act1": [0, 0, 0, 0, 0],
                    "act2": [0, 0, 0, 0, 0],
                    "act3": [0, 0, 0, 0, 0]
                }
            }

            # Write the JSON data to the file
            with open(file_path, "w") as output_file:
                json.dump(game_state_data, output_file, indent=4)

            return f"Game state file created: {file_path}"
        else:
            return f"Game state file already exists: {file_path}"
    except Exception as e:
        return f"Error initializing game state: {str(e)}"

# Example usage:
# initialize_game_state("your_game_code")


# Example usage:
# characters = ["detectivejohnson", "mselizabethblackwood", "professorarthurgrayson", "victoriavickyhart", "drjonathansmith", "emilyjohnson"]
# acts = ["act1", "act2", "act3"]
# num_tasks = 5
# initialize_game_state("IBJ7C", characters, acts, num_tasks)



def get_act(game_code):
        # Retrieve the current game state based on game_code
    file_path = os.path.join('staticfiles', 'chats', game_code, 'game_state.json')

    if not os.path.exists(file_path):
        # Handle the case where the game state doesn't exist (e.g., set act to 1)
        game_state = {"act": 1}
    else:
        with open(file_path, 'r') as file:
            game_state = json.load(file)

    # Get the current 'act' value from the game state
    current_act = game_state.get('act', 1)

    return current_act


def generate_game_code():
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random 5-character code
    game_code = ''.join(random.choice(characters) for _ in range(5))

    return game_code.upper()

import os
import json
from django.shortcuts import render

def lobby(request, game_code, character, chatee):
    # Concatenate character and chatee alphabetically
    sorted_names = sorted([character, chatee])
    concatenated_name = '_'.join(sorted_names)

    # Load chat history from the JSON file
    chat_history = load_chat_history(game_code, concatenated_name)

    return render(request, 'chat/lobby.html', {
        'game_code': game_code,
        'selected_character': character,
        'chatee': chatee,
        'concatenated_name': concatenated_name,
        'chat_history': chat_history  # Pass the chat history to the template
    })

def load_chat_history(game_code, characterpair):
    file_path = os.path.join('staticfiles', 'chats', game_code, f'{characterpair}.json')
    
    # Initialize an empty list if the file doesn't exist yet
    if not os.path.exists(file_path):
        chat_data = []
    else:
        # Load existing chat data from the file
        with open(file_path, 'r') as file:
            chat_data = json.load(file)
    
    return chat_data
from .data import get_character_info, get_act_info

def home_cookie(request):
    # Retrieve the selected character from the cookie
    selected_character = request.COOKIES.get('selectedCharacter', 'default_value')
    print(selected_character)
    data = get_character_info(selected_character)
    return render(request, 'chat/home.html', {'selected_character': data})


def home(request, game_code, character_name):
    
    current_act = get_act(game_code)

    act_details = get_act_info(str(current_act))

    if character_name:
        data = get_character_info(character_name)
        # Construct the template name based on the current_act value
        template_name = f'chat/home1.html'
        return render(request, template_name, {'selected_character': data, 'game_code': game_code, 'act_details': act_details, 'act': get_act(game_code)})

    # Retrieve the selected character from the cookie
    selected_character = request.COOKIES.get('selectedCharacter', '')
    data = get_character_info(selected_character)
    
    # Construct the template name based on the current_act value
    template_name = f'chat/home1.html'
    return render(request, template_name, {'selected_character': data, 'game_code': game_code ,'act_details': act_details, 'act': get_act(game_code)})


from .game_state import get_characters

def characters(request,game_code,selectedCharacter):

    your_context = get_characters(game_code)
    print(your_context  )
    return render(request, 'chat/characters.html',{ 'your_context' : your_context, 'game_code' : game_code, 'selectedCharacter': selectedCharacter})

import json

def checklist(request, game_code, character):
    try:
        tasks_file_path = os.path.join('staticfiles', 'chats', game_code, 'task.json')

        with open(tasks_file_path, 'r') as tasks_file:
            task_completion = json.load(tasks_file)
        
        task_description = os.path.join('chat/tasks.json')

        with open(task_description, 'r') as tasks_file1:
            task_data = json.load(tasks_file1)
        print(task_completion)
        tasks_completed = task_completion[character][f"act{get_act(game_code)}"]
        #output ['0,0,0,1,0']
        # Get tasks for the specific character and act

        current_act = str(get_act(game_code))
        character_tasks = task_data.get(character, {}).get(f"task{current_act}", [])
        checklist_data = []
        print(character_tasks)
        for task, is_completed in zip(character_tasks, tasks_completed):
            checklist_data.append((task, is_completed))
        print(checklist_data)
        return render(request, 'chat/checklist.html', {
            'data': checklist_data,
            'game_code': game_code,
            'character': character,
            
        })
    except FileNotFoundError:
        # Handle the case where tasks.json is not found
        return HttpResponse('Tasks data not found.', status=404)


def title(request):
    return render(request, 'chat/title.html')


def new_game(request):
    
    # Handle form submission and generate a 5-character game code
    if request.method == 'GET':
        game_code = generate_game_code()  # Implement your code to generate the code
        initialize_game_state(game_code)
        # Get the current working directory
        current_directory = os.getcwd()
        
        # Create a folder with the game code name relative to the working directory
        folder_path = os.path.join(current_directory, 'staticfiles', 'chats', game_code)
        print(folder_path)
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
        file_path = os.path.join('staticfiles', 'chats', game_code, 'waiting_room_state.json')
        print(file_path)
        if not os.path.exists(file_path):
            waiting_room_state = {
                'guy1': '',
                'girl1': '',
                'guy2': '',
                'girl2': '',
                'guy3': '',
                'girl3': '',
            }
        with open(file_path, 'w') as file:
            json.dump(waiting_room_state, file)
        request.session['game_code'] = game_code
        
        # Process the 'key' data as needed

        context = {'key': game_code , 'waiting_room_state' : read_json_file(file_path)}
        # Redirect or render the appropriate response
        return redirect('waiting_room')

    return render(request, 'chat/title.html')


from django.shortcuts import render, redirect

from django.shortcuts import render, redirect


import json

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
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create a logger instance
logger = logging.getLogger(__name__)


def waiting_room(request):

    if request.method == 'POST':
        # Handle the form submission
        key = request.POST.get('key', '').upper()  # Access the value of 'key' input field
        # Process the 'key' data as needed
        current_directory = os.getcwd()

        file_path = os.path.join(current_directory, 'staticfiles', 'chats', key,'waiting_room_state.json')    
        context = {'key': key , 'waiting_room_state' : read_json_file(file_path)}
        # Send a WebSocket message to the group
        channel_layer = get_channel_layer()
        room_group_name = f"chat_{key}"

        # Redirect or render the appropriate response
        return render(request, 'chat/waiting_room.html', context)
 # Redirect to another view  
    current_directory = os.getcwd()
    key = request.session.get('game_code', '')

    file_path = os.path.join(current_directory, 'staticfiles', 'chats', key,'waiting_room_state.json')    
    # Pass the 'key' variable to the template context}
    context = {'key': key , 'waiting_room_state' : read_json_file(file_path)}

    # Render the template with the context
    return render(request, 'chat/waiting_room.html', context)

# views.py
from django.http import JsonResponse
import os
import json

async def update_waiting_room(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            game_code = data.get('game_code')
            player_name = data.get('player_name')
            alt = data.get('alt')

            # Construct the path to the JSON file
            file_path = os.path.join('staticfiles', 'chats', game_code, 'waiting_room_state.json')
            print(file_path)
            if not os.path.exists(file_path):
                waiting_room_state = {
                    'guy1': '',
                    'girl1': '',
                    'guy2': '',
                    'girl2': '',
                    'guy3': '',
                    'girl3': '',
                }
            else:
                with open(file_path, 'r') as file:
                    waiting_room_state = json.load(file)

            waiting_room_state[alt] = player_name

            with open(file_path, 'w') as file:
                json.dump(waiting_room_state, file)        
            try:
                channel_layer = get_channel_layer()
                channel_id = id(channel_layer)  # Get the ID of the channel layer instance
                print(f"View Channel ID: {channel_id}")
            
                print(str(channel_layer))
                room_group_name = f"chat_{game_code}"
                print(f"Room group name: {room_group_name}")  # Log a debug message
                context = {'key': game_code , 'waiting_room_state' : read_json_file(file_path)}
                print(c)
                await channel_layer.group_add(room_group_name, channel_layer)
                channel_layer.group_send(
                room_group_name,
                {
                    'type': "connected",
                    'message': context,
                }
            )
                # ... rest of your code ...

            except Exception as e:
                print(f"An error occurred: {str(e)}")  # Log an error message
                return JsonResponse({'success': False, 'error_message': str(e)})
            return JsonResponse({'success': True, 'message': 'Data updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

# views.py
from django.http import JsonResponse
import os
import json

# views.py
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import os
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def update_game_state(request,game_code):
    print('eeeee')
    try:

        # Construct the path to the JSON file based on the game code
        file_path = os.path.join('staticfiles', 'chats', game_code, 'game_state.json')
        
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it with "act": 1
            game_state = {"act": 1 }
        else:
            with open(file_path, 'r') as file:
                game_state = json.load(file)
            
            # Increment the "act" value by one
            game_state['act'] += 1

        with open(file_path, 'w') as file:
            json.dump(game_state, file)


        return JsonResponse({'success': True, 'act': game_state['act']})

    except Exception as e:
        print("no luck")
        return JsonResponse({'success': False, 'error_message': str(e)})
 

def act1(request,game_code,character):
    current_act = get_act(game_code)
    print(current_act)
    return render(request, 'chat/act1video.html', {'game_code': game_code, 'selected_character': character, 'act': current_act })
from django.http import JsonResponse

def end(request,game_code,character):
    current_act = get_act(game_code)
    print(current_act)
    return render(request, 'chat/end.html', {'game_code': game_code, 'selected_character': character, 'act': current_act })
from django.http import JsonResponse
# from .models import ChatMessage

# def load_messages(request, game_code, character):
#     # Assuming concatenated_name is the character pair
#     messages = ChatMessage.objects.filter(game_code=game_code, characterpair=character).order_by('timestamp')
#     message_list = [{'message': message.message} for message in messages]
#     return JsonResponse({'messages': message_list})
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt  # Add CSRF exemption if needed
# import json

# @csrf_exempt  # Add CSRF exemption if needed
# def save_message(request, game_code, characterpair,character):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             message_text = data.get('message', '')

#             if message_text:
#                 ChatMessage.objects.create(
#                     game_code=game_code,
#                     characterpair=characterpair,
#                     character=character,
#                     message=message_text
#                 )

#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})
