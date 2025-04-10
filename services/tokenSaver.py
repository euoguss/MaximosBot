import json
import os

def save_token(chat_id, token_data):
    file_path = "tokens.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            tokens = json.load(f)
    else:
        tokens = {}

    tokens[chat_id] = token_data

    with open(file_path, "w") as f:
        json.dump(tokens, f, indent=2)

def load_token(chat_id):
    file_path = "tokens.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            tokens = json.load(f)
        return tokens.get(chat_id)
    return None