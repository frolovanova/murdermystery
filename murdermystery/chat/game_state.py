import os
    
import json

def get_characters(game_code):
    current_directory = os.getcwd()

    json_file_path = os.path.join(current_directory, 'staticfiles', 'chats', game_code,'waiting_room_state.json')

    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        non_empty_pairs = {key: value for key, value in data.items() if value != ""}
        return non_empty_pairs
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}